# Pruna nodes for ComfyUI

This repository contains a custom compilation node for ComfyUI that accelerates Stable Diffusion (SD) and Flux inference using Pruna. 

## Installation

### Prerequisites
1. Create a new conda environment with Python 3.10
2. Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
3. Install the latest version of [Pruna](https://docs.pruna.ai/en/latest/setup/pip.html)
4. Generate a Pruna token, following the instructions [here](https://docs.pruna.ai/en/latest/setup/token.html)

### Steps
1. Navigate to your ComfyUI installation's `custom_nodes` folder
2. Clone this repository
3. Launch ComfyUI

The Pruna node will appear in the nodes menu in the `Pruna` category. 

**Important note**: The current implementation requires launching ComfyUI with the `--disable-cuda-malloc` flag; 
otherwise the node may not function properly. For optimal performance, we also recommend setting the 
`--gpu-only` flag. These flags can be added when starting ComfyUI from the command line:
```bash
python main.py --disable-cuda-malloc --gpu-only
```


## Usage Example

We provide two example workflows: one using an SD model and another based on Flux. 

To load the  workflow:
- Drag and drop the provided `.json` file from the `workflows` folder into the ComfyUI window, or
- Click `Open` in the `Workflow` tab (top-left corner of ComfyUI)

Through the GUI, you can choose your preferred compilation mode. Currently, we support `x-fast` and `torch_compile` with `torch_compile` set as the default.


### Model Setup

#### Stable Diffusion
You have two options for the base model:

##### Option 1: SafeTensors Format (Recommended)
1. Download the [safetensors version](https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/refs%2Fpr%2F228/sd-v1-4.safetensors) from Hugging Face
2. Place it in `<path_to_comfyui>/models/checkpoints`

##### Option 2: Diffusers Format
1. Download the Diffusers version of SD v1.4
2. Place it in `<path_to_comfyui>/models/diffusers`
3. Replace the `Load Checkpoint` node with a `DiffusersLoader` node

The node is tested using the SafeTensors format, so for the 
sake of reproducibility, we recommend using that format. 
However, we don't expect any performance differences between the two.

![Example Workflow](./images/SD.png)

#### Flux 
To use Flux, you must separately download all model components—including the VAE, CLIP, and diffusion model weights—and place them in the appropriate folder.
You can follow [these instructions](https://comfyanonymous.github.io/ComfyUI_examples/flux/)
as a guide. Note that in this example, we use the full regular version. 

![Example Workflow](./images/flux.png)

## Performance

The node was tested on an NVIDIA L40S GPU. Below, we present a comparison of the performance between the compiled and uncompiled models.  
- The first figure presents the performance in iterations per second, as reported by `ComfyUI`.
- The second figure shows the end-to-end time required to generate a single image.

![Performance](./images/performance_its.png)
![Performance](./images/performance_end2end.png)

## Contact

For any questions or feedback, feel free to join our [Discord](https://discord.com/invite/Tun8YgzxZ9).
We have a dedicated *help-desk* channel, and you're welcome to engage with our community. 

