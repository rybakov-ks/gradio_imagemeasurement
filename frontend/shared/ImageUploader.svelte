<script lang="ts">
	import { createEventDispatcher, tick } from "svelte";
	import { BlockLabel, IconButtonWrapper, IconButton } from "@gradio/atoms";
	import { Clear, Image as ImageIcon, ZoomIn, ZoomOut, Redo } from "@gradio/icons";
	import { FullscreenButton } from "@gradio/atoms";
	import {
		type SelectData,
		type I18nFormatter,
		type ValueData
	} from "@gradio/utils";
	import { get_coordinates_of_clicked_image } from "./utils";
	import Webcam from "./Webcam.svelte";

	import { Upload, UploadProgress } from "@gradio/upload";
	import { FileData, type Client } from "@gradio/client";
	import { SelectSource } from "@gradio/atoms";
	import Image from "./Image.svelte";
	import type { Base64File, WebcamOptions } from "./types";

	interface Point {
		x: number;
		y: number;
	}

	interface MeasurementData {
		point_a: Point | null;
		point_b: Point | null;
		distance_px: number | null;
	}

	let points: Point[] = [];
	let scale: number = 1;
	const scaleStep: number = 0.2;
	const MAX_SCALE = 5;
	
	let imageContainer: HTMLDivElement;
	let isImageLoaded: boolean = false;

	export let measurement_mode: boolean = true;

	let imageElement: HTMLImageElement | null = null;

	function getImageCoordinates(event: MouseEvent): Point | null {
		if (!imageElement || !(imageElement instanceof HTMLImageElement)) {
			return null;
		}
		
		const img = imageElement;
		const rect = img.getBoundingClientRect();
		
		if (img.naturalWidth === 0 || img.naturalHeight === 0) {
			return null;
		}
		
		const x_screen = event.clientX - rect.left;
		const y_screen = event.clientY - rect.top;
		
		let x = Math.floor(x_screen * (img.naturalWidth / rect.width));
		let y = Math.floor(y_screen * (img.naturalHeight / rect.height));
		
		if (points.length === 1) {
			y = points[0].y;
		}
		
		if (x < 0 || y < 0 || x > img.naturalWidth || y > img.naturalHeight) {
			return null;
		}
		
		return { x, y };
	}

	function handleMeasurementClick(event: MouseEvent): void {
		if (!value || !isImageLoaded || !measurement_mode) {
			return;
		}

		const point = getImageCoordinates(event);
		
		if (!point) {
			return;
		}

		if (points.length >= 2) {
			points = [point];
		} else {
			points = [...points, point];
		}

		if (points.length === 2) {
			const distance = calculateDistance(points[0], points[1]);
			const measurementData: MeasurementData = {
				point_a: points[0],
				point_b: points[1], 
				distance_px: distance
			};
			dispatch("measurement", measurementData);
		}
	}

	function handleImageLoad(event: Event): void {
		const imgElement = event.target as HTMLImageElement;
		imageElement = imgElement;
		isImageLoaded = true;
		scale = 1; 
		if (imageContainer) {
			imageContainer.scrollLeft = 0;
			imageContainer.scrollTop = 0;
		}
	}

	function calculateDistance(point1: Point, point2: Point): number {
		const dx = point2.x - point1.x;
		const dy = point2.y - point1.y;
		return Math.round(Math.sqrt(dx * dx + dy * dy));
	}

	function zoomIn(): void {
		scale = Math.min(scale + scaleStep, MAX_SCALE);
	}

	function zoomOut(): void {
		scale = Math.max(scale - scaleStep, 1);
		if (scale === 1 && imageContainer) {
			imageContainer.scrollLeft = 0;
			imageContainer.scrollTop = 0;
		}
	}

	function resetMeasurement(): void {
		scale = 1;
		if (imageContainer) {
			imageContainer.scrollLeft = 0;
			imageContainer.scrollTop = 0;
		}
	}

	$: if (value && measurement_mode) {
		points = [];
		resetMeasurement();
	}

	export let value: null | FileData | Base64File = null;
	export let label: string | undefined = undefined;
	export let show_label: boolean;

	type source_type = "upload" | "webcam" | "clipboard" | "microphone" | null;

	export let sources: source_type[] = ["upload", "clipboard", "webcam"];
	export let streaming = false;
	export let pending = false;
	export let webcam_options: WebcamOptions;
	export let selectable = false;
	export let root: string;
	export let i18n: I18nFormatter;
	export let max_file_size: number | null = null;
	export let upload: Client["upload"];
	export let stream_handler: Client["stream"];
	export let stream_every: number;

	export let modify_stream: (state: "open" | "closed" | "waiting") => void;
	export let set_time_limit: (arg0: number) => void;
	export let show_fullscreen_button = true;

	let upload_input: Upload;
	export let uploading = false;
	export let active_source: source_type = null;
	export let fullscreen = false;

	let files: FileData[] = [];
	let upload_id: string;

	async function handle_upload({
		detail
	}: CustomEvent<FileData>): Promise<void> {
		if (!streaming) {
			if (detail.path?.toLowerCase().endsWith(".svg") && detail.url) {
				const response = await fetch(detail.url);
				const svgContent = await response.text();
				value = {
					...detail,
					url: `data:image/svg+xml,${encodeURIComponent(svgContent)}`
				};
			} else {
				value = detail;
			}

			await tick();
			dispatch("upload");
		}
	}

	function handle_clear(): void {
		value = null;
		points = [];
		isImageLoaded = false;
		dispatch("clear");
		dispatch("change", null);
	}

	function handle_remove_image_click(event: MouseEvent): void {
		handle_clear();
		event.stopPropagation();
	}

	async function handle_save(
		img_blob: Blob | any,
		event: "change" | "stream" | "upload"
	): Promise<void> {
		if (event === "stream") {
			dispatch("stream", {
				value: { url: img_blob } as Base64File,
				is_value_data: true
			});
			return;
		}
		upload_id = Math.random().toString(36).substring(2, 15);
		const f_ = new File([img_blob], `image.${streaming ? "jpeg" : "png"}`);
		files = [
			new FileData({
				path: f_.name,
				orig_name: f_.name,
				blob: f_,
				size: f_.size,
				mime_type: f_.type,
				is_stream: false
			})
		];
		pending = true;
		const f = await upload_input.load_files([f_], upload_id);
		if (event === "change" || event === "upload") {
			value = f?.[0] || null;
			await tick();
			dispatch("change");
		}
		pending = false;
	}

	$: active_streaming = streaming && active_source === "webcam";
	$: if (uploading && !active_streaming) value = null;

	const dispatch = createEventDispatcher<{
		change?: never;
		stream: ValueData;
		clear?: never;
		drag: boolean;
		upload?: never;
		select: SelectData;
		end_stream: never;
		measurement: MeasurementData;
	}>();

	export let dragging = false;

	$: dispatch("drag", dragging);

	function handle_click(evt: MouseEvent): void {
		if (measurement_mode) {
			handleMeasurementClick(evt);
		} else {
			let coordinates = get_coordinates_of_clicked_image(evt);
			if (coordinates) {
				dispatch("select", { index: coordinates, value: null });
			}
		}
	}

	$: if (!active_source && sources) {
		active_source = sources[0];
	}

	async function handle_select_source(
		source: (typeof sources)[number]
	): Promise<void> {
		switch (source) {
			case "clipboard":
				upload_input.paste_clipboard();
				break;
			default:
				break;
		}
	}

	let image_container: HTMLElement;

	function on_drag_over(evt: DragEvent): void {
		evt.preventDefault();
		evt.stopPropagation();
		if (evt.dataTransfer) {
			evt.dataTransfer.dropEffect = "copy";
		}

		dragging = true;
	}

	async function on_drop(evt: DragEvent): Promise<void> {
		evt.preventDefault();
		evt.stopPropagation();
		dragging = false;

		if (value) {
			handle_clear();
			await tick();
		}

		active_source = "upload";
		await tick();
		upload_input.load_files_from_drop(evt);
	}
</script>

<BlockLabel {show_label} Icon={ImageIcon} label={label || "Image"} />

<div data-testid="image" class="image-container" bind:this={image_container}>
	<IconButtonWrapper>
		{#if value?.url && !active_streaming}
			{#if show_fullscreen_button}
				<FullscreenButton {fullscreen} on:fullscreen />
			{/if}
			<IconButton
				Icon={Clear}
				label="Remove Image"
				on:click={handle_remove_image_click}
			/>
		{/if}
	</IconButtonWrapper>
	<div
		class="upload-container"
		class:reduced-height={sources.length > 1}
		style:width={value ? "auto" : "100%"}
		on:dragover={on_drag_over}
		on:drop={on_drop}
		role="application"
		aria-label={i18n("image.drop_to_upload")}
	>
		<Upload
			hidden={value !== null || active_source === "webcam"}
			bind:this={upload_input}
			bind:uploading
			bind:dragging
			filetype={active_source === "clipboard" ? "clipboard" : "image/*"}
			on:load={handle_upload}
			on:error
			{root}
			{max_file_size}
			disable_click={!sources.includes("upload") || value !== null}
			{upload}
			{stream_handler}
			aria_label={i18n("image.drop_to_upload")}
		>
			{#if value === null}
				<slot />
			{/if}
		</Upload>
		{#if active_source === "webcam" && !streaming && pending}
			<UploadProgress {root} {upload_id} {stream_handler} {files} />
		{:else if active_source === "webcam" && (streaming || (!streaming && !value))}
			<Webcam
				{root}
				{value}
				on:capture={(e) => handle_save(e.detail, "change")}
				on:stream={(e) => handle_save(e.detail, "stream")}
				on:error
				on:drag
				on:upload={(e) => handle_save(e.detail, "upload")}
				on:close_stream
				mirror_webcam={webcam_options.mirror}
				{stream_every}
				{streaming}
				mode="image"
				include_audio={false}
				{i18n}
				{upload}
				bind:modify_stream
				bind:set_time_limit
				webcam_constraints={webcam_options.constraints}
			/>
		{:else if value !== null}
			{#if measurement_mode}
				<div class="measurement-wrapper">
					<div 
						class="image-measurement-container" 
						bind:this={imageContainer}
						style="overflow: {scale > 1.001 ? 'auto' : 'hidden'};" 
					>
						<div 
							class="scaled-wrapper"
							style="transform: scale({scale});"
						>
							<div class="image-with-overlay">
								<div 
									class="image-frame measurement-image-frame" 
									on:click={handle_click}
									on:keydown={(e) => { if (e.key === 'Enter' || e.key === ' ') handle_click(e) }}
									role="button"
									tabindex="0"
									aria-label={i18n("image.select_points")}
								>
									<Image 
										src={value.url} 
										alt={value.alt_text}
										on:load={handleImageLoad}
										class="measurement-image"
									/>
								</div>
								
								{#if value && value.url && (imageElement || isImageLoaded)}
									<svg 
										class="measurement-overlay"
										viewBox={`0 0 ${imageElement.naturalWidth} ${imageElement.naturalHeight}`}
										preserveAspectRatio="none"
										style="width: 100%; height: 100%;"
									>
										{#if points.length === 2}
											{@const baseSize = Math.max(imageElement.naturalWidth, imageElement.naturalHeight) / 100}
											<line 
												x1={points[0].x} 
												y1={points[0].y} 
												x2={points[1].x} 
												y2={points[1].y} 
												stroke="#00ff00" 
												stroke-width={baseSize * 0.5}
												stroke-dasharray={`${baseSize * 1.2},${baseSize * 0.6}`}
											/>
											<text 
												x={(points[0].x + points[1].x) / 2} 
												y={(points[0].y + points[1].y) / 2 - baseSize * 2.5} 
												fill="#00ff00" 
												font-size={baseSize * 2.5}
												font-weight="bold"
												text-anchor="middle"
												stroke="black"
												stroke-width={baseSize * 0.4}
												paint-order="stroke"
											>
												{calculateDistance(points[0], points[1])} px
											</text>
										{/if}
										
										{#each points as point, i}
											{@const baseSize = Math.max(imageElement.naturalWidth, imageElement.naturalHeight) / 100}
											<circle 
												cx={point.x} 
												cy={point.y} 
												r={baseSize * 0.8}
												fill={i === 0 ? '#ff0000' : '#0000ff'}
											/>
											<text 
												x={point.x} 
												y={point.y - baseSize * 0.1} 
												fill="white" 
												font-size={baseSize * 1.8}
												font-weight="bold"
												text-anchor="middle"
												dominant-baseline="central"
											>
												{i + 1}
											</text>
										{/each}
									</svg>
								{/if}
							</div>
						</div>
					</div>
					
					{#if value && value.url}
						<div class="measurement-controls">
							<IconButton 
								Icon={ZoomIn} 
								label="ZoomIn"
								disabled={scale >= MAX_SCALE}
								on:click={zoomIn}
							/>
							<IconButton 
								Icon={ZoomOut} 
								label="ZoomOut"
								disabled={scale <= 1}
								on:click={zoomOut}
							/>
							<IconButton 
								Icon={Redo} 
								label="Reset"
								on:click={resetMeasurement}
							/>
							<span class="scale-info">{Math.round(scale * 100)}%</span>
							{#if points.length > 0}
								<span class="points-info">{points.length}/2</span>
							{/if}
						</div>
					{/if}
				</div>
			{:else}
				<div 
					class:selectable 
					class="image-frame" 
					on:click={handle_click}
					on:keydown={(e) => { if (e.key === 'Enter' || e.key === ' ') handle_click(e) }}
					role="button"
					tabindex="0"
					aria-label={i18n("image.select_points")}
				>
					<Image src={value.url} alt={value.alt_text} />
				</div>
			{/if}
		{/if}
	</div>
	{#if sources.length > 1 || sources.includes("clipboard")}
		<SelectSource
			{sources}
			bind:active_source
			{handle_clear}
			handle_select={handle_select_source}
		/>
	{/if}
</div>

<style>
	.image-frame :global(img) {
		width: var(--size-full);
		height: var(--size-full);
		object-fit: scale-down;
	}

	.upload-container {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100%;
		flex-shrink: 1;
		max-height: 100%;
	}

	.reduced-height {
		height: calc(100% - var(--size-10));
	}

	.image-container {
		display: flex;
		height: 100%;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		max-height: 100%;
	}

	.selectable {
		cursor: crosshair;
	}

	.image-frame {
		object-fit: cover;
		width: 100%;
		height: 100%;
	}
	
	.image-frame:focus {
		outline: 2px solid var(--color-primary-500);
		outline-offset: 2px;
	}

	.measurement-wrapper {
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	.image-measurement-container {
		flex: 1;
		position: relative;
		min-height: 0;
		display: flex; 
		align-items: center;
		justify-content: center;
		background: var(--color-grey-50);
	}

	.scaled-wrapper {
		display: block;
		transform-origin: 0 0;
		transition: transform 0.2s ease-out; 
		flex-shrink: 0; 
		max-width: 100%; 
		max-height: 100%;
	}
	
	.image-with-overlay {
		position: relative;
		display: block;
		line-height: 0; 
		max-width: 100%;
		max-height: 100%;
		flex-shrink: 1;
	}
	
	.measurement-image-frame {
		background: transparent;
		cursor: crosshair;
	}
	
	.measurement-image-frame:focus {
		outline: 2px solid var(--color-primary-500);
		outline-offset: 2px;
	}
	
	.measurement-overlay {
		position: absolute;
		top: 0;
		left: 0;
		pointer-events: none; 
		z-index: 10;
		width: 100%;
		height: 100%;
	}

	.measurement-controls {
		padding: var(--size-2) var(--size-3);
		background: var(--block-background-fill);
		border-top: 1px solid var(--block-border-color);
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--spacing-sm);
		flex-wrap: wrap;
		flex-shrink: 0;
		z-index: 5;
	}
	
	.scale-info, .points-info {
		font-size: var(--text-sm);
		color: var(--block-label-text-color);
		margin-left: var(--spacing-sm);
		font-weight: var(--block-label-text-weight);
	}
</style>