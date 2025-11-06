
import gradio as gr
from app import demo as app
import os

_docs = {'ImageMeasurement': {'description': 'Creates an image component that can be used to upload images (as an input) or display images (as an output).\n', 'members': {'__init__': {'value': {'type': 'str | PIL.Image.Image | np.ndarray | Callable | None', 'default': 'None', 'description': 'A `PIL.Image`, `numpy.array`, `pathlib.Path`, or `str` filepath or URL for the default value that ImageMeasurement component is going to take. If a function is provided, the function will be called each time the app loads to set the initial value of this component.'}, 'format': {'type': 'str', 'default': '"webp"', 'description': 'File format (e.g. "png" or "gif"). Used to save image if it does not already have a valid format (e.g. if the image is being returned to the frontend as a numpy array or PIL ImageMeasurement). The format should be supported by the PIL library. Applies both when this component is used as an input or output. This parameter has no effect on SVG files.'}, 'height': {'type': 'int | str | None', 'default': 'None', 'description': 'The height of the component, specified in pixels if a number is passed, or in CSS units if a string is passed. This has no effect on the preprocessed image file or numpy array, but will affect the displayed image.'}, 'width': {'type': 'int | str | None', 'default': 'None', 'description': 'The width of the component, specified in pixels if a number is passed, or in CSS units if a string is passed. This has no effect on the preprocessed image file or numpy array, but will affect the displayed image.'}, 'image_mode': {'type': 'Literal[\n        "1",\n        "L",\n        "P",\n        "RGB",\n        "RGBA",\n        "CMYK",\n        "YCbCr",\n        "LAB",\n        "HSV",\n        "I",\n        "F",\n    ]\n    | None', 'default': '"RGB"', 'description': 'The pixel format and color depth that the image should be loaded and preprocessed as. "RGB" will load the image as a color image, or "L" as black-and-white. See https://pillow.readthedocs.io/en/stable/handbook/concepts.html for other supported image modes and their meaning. This parameter has no effect on SVG or GIF files. If set to None, the image_mode will be inferred from the image file type (e.g. "RGBA" for a .png image, "RGB" in most other cases).'}, 'sources': {'type': 'list[Literal["upload", "webcam", "clipboard"]]\n    | Literal["upload", "webcam", "clipboard"]\n    | None', 'default': 'None', 'description': 'List of sources for the image. "upload" creates a box where user can drop an image file, "webcam" allows user to take snapshot from their webcam, "clipboard" allows users to paste an image from the clipboard. If None, defaults to ["upload", "webcam", "clipboard"] if streaming is False, otherwise defaults to ["webcam"].'}, 'type': {'type': 'Literal["numpy", "pil", "filepath"]', 'default': '"numpy"', 'description': 'The format the image is converted before being passed into the prediction function. "numpy" converts the image to a numpy array with shape (height, width, 3) and values from 0 to 255, "pil" converts the image to a PIL image object, "filepath" passes a str path to a temporary file containing the image. To support animated GIFs in input, the `type` should be set to "filepath" or "pil". To support SVGs, the `type` should be set to "filepath".'}, 'label': {'type': 'str | I18nData | None', 'default': 'None', 'description': 'the label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'every': {'type': 'Timer | float | None', 'default': 'None', 'description': 'Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.'}, 'inputs': {'type': 'Component | Sequence[Component] | set[Component] | None', 'default': 'None', 'description': 'Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.'}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'show_download_button': {'type': 'bool', 'default': 'True', 'description': 'If True, will display button to download image. Only applies if interactive is False (e.g. if the component is used as an output).'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will allow users to upload and edit an image; if False, can only be used to display images. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool | Literal["hidden"]', 'default': 'True', 'description': 'If False, component will be hidden. If "hidden", component will be visually hidden and not take up space in the layout but still exist in the DOM'}, 'streaming': {'type': 'bool', 'default': 'False', 'description': "If True when used in a `live` interface, will automatically stream webcam feed. Only valid is source is 'webcam'. If the component is an output component, will automatically convert images to base64."}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | tuple[int | str, ...] | None', 'default': 'None', 'description': "in a gr.render, Components with the same key across re-renders are treated as the same component, not a new component. Properties set in 'preserved_by_key' are not reset across a re-render."}, 'preserved_by_key': {'type': 'list[str] | str | None', 'default': '"value"', 'description': "A list of parameters from this component's constructor. Inside a gr.render() function, if a component is re-rendered with the same key, these (and only these) parameters will be preserved in the UI (if they have been changed by the user or an event listener) instead of re-rendered based on the values provided during constructor."}, 'mirror_webcam': {'type': 'bool | None', 'default': 'None', 'description': 'If True webcam will be mirrored. Default is True.'}, 'webcam_options': {'type': 'WebcamOptions | None', 'default': 'None', 'description': None}, 'show_share_button': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.'}, 'placeholder': {'type': 'str | None', 'default': 'None', 'description': 'Custom text for the upload area. Overrides default upload messages when provided. Accepts new lines and `#` to designate a heading.'}, 'show_fullscreen_button': {'type': 'bool', 'default': 'True', 'description': 'If True, will show a fullscreen icon in the corner of the component that allows user to view the image in fullscreen mode. If False, icon does not appear.'}, 'webcam_constraints': {'type': 'dict[str, Any] | None', 'default': 'None', 'description': "A dictionary that allows developers to specify custom media constraints for the webcam stream. This parameter provides flexibility to control the video stream's properties, such as resolution and front or rear camera on mobile devices. See $demo/webcam_constraints"}, 'watermark': {'type': 'WatermarkOptions | None', 'default': 'None', 'description': 'If provided and this component is used to display a `value` image, the `watermark` image will be displayed on the bottom right of the `value` image, 10 pixels from the bottom and 10 pixels from the right. The watermark image will not be resized. Supports `PIL.Image`, `numpy.array`, `pathlib.Path`, and `str` filepaths. SVGs and GIFs are not supported as `watermark` images nor can they be watermarked.'}}, 'postprocess': {'value': {'type': 'numpy.ndarray | PIL.Image.Image | str | pathlib.Path | None', 'description': 'Expects a `numpy.array`, `PIL.Image`, or `str` or `pathlib.Path` filepath to an image which is displayed.'}}, 'preprocess': {'return': {'type': 'numpy.ndarray | PIL.Image.Image | str | None', 'description': 'Passes the uploaded image as a `numpy.array`, `PIL.Image` or `str` filepath depending on `type`.'}, 'value': None}}, 'events': {'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the ImageMeasurement using the clear button for the component.'}, 'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the ImageMeasurement changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'stream': {'type': None, 'default': None, 'description': 'This listener is triggered when the user streams the ImageMeasurement.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the ImageMeasurement. Uses event data gradio.SelectData to carry `value` referring to the label of the ImageMeasurement, and `selected` to refer to state of the ImageMeasurement. See EventData documentation on how to use this event data'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the ImageMeasurement.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the ImageMeasurement.'}, 'measurement': {'type': None, 'default': None, 'description': "This listener is triggered when the user completes a measurement by clicking two points on the image. \n        The event data contains the coordinates of both points and the calculated distance in pixels.\n        \n        Returns:\n            dict: Measurement data with the following structure:\n            {\n                'point_a': {'x': int, 'y': int},  # Coordinates of first point\n                'point_b': {'x': int, 'y': int},  # Coordinates of second point  \n                'distance_px': int                # Distance between points in pixels\n            }\n        "}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'ImageMeasurement': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_imagemeasurement`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

A component for measuring the distance in pixels between two points in an image.
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_imagemeasurement
```

## Usage

```python
import gradio as gr
from gradio_imagemeasurement import ImageMeasurement

def show_measurement(image_input,  data: gr.EventData):
    if data._data and 'distance_px' in  data._data:
        return f"{data._data}"
    return "Click two dots on the image"

with gr.Blocks() as demo:
    gr.Markdown("# ImageMeasurement")
    gr.Markdown("Click two points on the image to measure the distance.")
    
    with gr.Row():
        image_input = ImageMeasurement(label="Image", sources="upload")
        result = gr.Textbox(label="Result")
        
    gr.Examples(
        examples=[
            "https://raw.githubusercontent.com/rybakov-ks/ParticleAnalyzer/refs/heads/main/example/Cathode_LiCoVO4.jpg",
            "https://raw.githubusercontent.com/rybakov-ks/ParticleAnalyzer/refs/heads/main/example/Chitosan.webp",
            "https://raw.githubusercontent.com/rybakov-ks/ParticleAnalyzer/refs/heads/main/example/Silicon_oxide.webp",
            "https://raw.githubusercontent.com/rybakov-ks/ParticleAnalyzer/refs/heads/main/example/Gold_on_carbon.jpg",
            "https://raw.githubusercontent.com/rybakov-ks/ParticleAnalyzer/refs/heads/main/example/Colloidal_silver.webp",
        ],
        example_labels=[
            "Cathode material LiCoVO₄",
            "Chitosan nanoparticles",
            "Silicon oxide",
            "Gold on carbon",
            "Colloidal silver",
        ],
        inputs=[image_input],
        label="Examples",
        elem_id="examples_images",
    )

    image_input.measurement(fn=show_measurement, inputs=image_input, outputs=result)  

if __name__ == "__main__":
    demo.launch()
```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `ImageMeasurement`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["ImageMeasurement"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["ImageMeasurement"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the uploaded image as a `numpy.array`, `PIL.Image` or `str` filepath depending on `type`.
- **As output:** Should return, expects a `numpy.array`, `PIL.Image`, or `str` or `pathlib.Path` filepath to an image which is displayed.

 ```python
def predict(
    value: numpy.ndarray | PIL.Image.Image | str | None
) -> numpy.ndarray | PIL.Image.Image | str | pathlib.Path | None:
    return value
```
""", elem_classes=["md-custom", "ImageMeasurement-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          ImageMeasurement: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
