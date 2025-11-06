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