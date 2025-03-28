# Pruna nodes for ComfyUI

This repository explains how to accelerate image generation in ComfyUI using **Pruna**, an inference optimization engine that makes AI models **faster, smaller, cheaper, and greener**. ComfyUI is a popular node-based GUI for image generation models, for which we provide two custom nodes:
- a **compilation node**, that optimizes inference speed through model compilation, without compromising output quality.
- a **caching node** that smartly reuses intermediate computations to accelerate inference with minimal quality degradation.

Both of them can be applied to **Stable Diffusion (SD)** and **Flux** models. 


Here, you'll find:
- [Installation and usage instructions](#installation)
- [Representative workflows](#usage)
- [Performance benchmarks](#performance)

## Installation

### Prerequisites
1. Create a new conda environment
2. Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI/?tab=readme-ov-file#installing)
3. Install the latest version of [Pruna or Pruna Pro](https://docs.pruna.ai/en/stable/setup/pip.html)
4. For Pruna Pro, after [requesting a token](https://docs.pruna.ai/en/stable/setup/pip.html#installing-pruna-pro), you should export the token as an environment variable:

```bash
export PRUNA_TOKEN=<your_token_here>
```


> **Note:** *Pruna Pro is required* to use the caching node or the `x_fast` compilation mode.

### Steps
1. **Navigate to your ComfyUI installation's `custom_nodes` folder:**
```bash
cd <path_to_comfyui>/custom_nodes
```
2. **Clone this repository:**
```bash
git clone https://github.com/PrunaAI/ComfyUI_pruna.git
```
3. **Launch ComfyUI**, for example, with:
```bash
cd <path_to_comfyui> && python main.py --disable-cuda-malloc --gpu-only
```

The Pruna node will appear in the nodes menu in the `Pruna` category. 

**Important note**: The compilation node requires launching ComfyUI with the `--disable-cuda-malloc` flag; 
otherwise the node may not function properly. For optimal performance, we also recommend setting the 
`--gpu-only` flag. 

## Usage 

### Workflows 

We provide two types of workflows: one using a [Stable Diffusion](#example-1-stable-diffusion) model and another based on [Flux](#example-2-flux). 
To these models, we apply caching, compilation or their combination. 

| Optimization Technique                     | Stable Diffusion | Flux |
|--------------------------|-----------------|------|
| **Compilation**          | [SD Compilation](./workflows/SD_compile.json) ([Preview](./images/SD_compile.png)) | [Flux Compilation](./workflows/flux_compile.json) ([Preview](./images/flux_compile.png)) |
| **Caching**              | [SD Caching](./workflows/SD_caching.json) ([Preview](./images/SD_caching.png)) | [Flux Caching](./workflows/flux_caching.json) ([Preview](./images/flux_caching.png)) |
| **Caching + Compilation** | [SD Caching + Compilation](./workflows/SD_compile+caching.json) ([Preview](./images/SD_compile+caching.png)) | [Flux Caching + Compilation](./workflows/flux_compile+caching.json) ([Preview](./images/flux_compile+caching.png)) |


To load the  workflow:
- Drag and drop the provided json file into the ComfyUI window
- **OR** Click `Open` in the `Workflow` tab, as shown [here](./images/comfy_gui.png), and select the file

To run the workflow, make sure that you have first [set up the desired model](#model-setup).

### Model Setup

#### Example 1: Stable Diffusion

You have two options for the base model:

##### Option 1: SafeTensors Format (Recommended)
1. Download the [safetensors version](https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/refs%2Fpr%2F228/sd-v1-4.safetensors) 
2. Place it in `<path_to_comfyui>/models/checkpoints`

##### Option 2: Diffusers Format
1. Download the Diffusers version of SD v1.4
2. Place it in `<path_to_comfyui>/models/diffusers`
3. Replace the `Load Checkpoint` node with a `DiffusersLoader` node

The node is tested using the SafeTensors format, so for the sake of reproducibility, we recommend using that format. However, we don't expect any performance differences between the two.

After loading the model, you can [choose the desired workflow](#workflows), and you're all set!

**Note**: In this example, we use the [Stable Diffusion v1.4](https://huggingface.co/CompVis/stable-diffusion-v-1-4-original) model. However, our nodes are compatible with any other SD model — feel free to use your favorite one!


#### Example 2: Flux
To use Flux, you must separately download all model components—including the VAE, CLIP, and diffusion model weights—and place them in the appropriate folder. 

**Steps to set up Flux:**
1. **For the CLIP models:** Get the following files:
    - [clip_l.safetensors](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/clip_l.safetensors)
    - [t5xxl_fp16.safetensors](https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/t5xxl_fp16.safetensors)

    Move them to `<path_to_comfyui>/models/clip/`.
2. **For the VAE model:** 
Get the [VAE](https://huggingface.co/black-forest-labs/FLUX.1-schnell/blob/main/ae.safetensors) model, and move it to `<path_to_comfyui>/models/vae/` directory. 
3. **For the Flux model:** 
You first need to request access to the model [here](https://huggingface.co/black-forest-labs/FLUX.1-dev). Once you have access, download the [weights](https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/flux1-dev.safetensors) and move them to `<path_to_comfyui>/models/diffusion_models/`. 

Now, just load the [workflow](#workflows) and you're ready to go!


### Hyperparameters

Through the GUI, you can configure various **optimization settings**. Specifically:

- **Compilation**: We currently support two compilation modes: `x_fast` and `torch_compile`, with `x_fast` set as the default.
- **Caching**: Our caching mechanism supports the `adaptive` algorithm, which allows you to adjust the `threshold` and `max_skip_steps` parameters:
  - **`threshold`**: Acceptable values range from `0.001` to `0.2`.  
  - **`max_skip_steps`**: Acceptable values range from `1` to `5`.  

  We recommend using the default values (`threshold = 0.01`, `max_skip_steps = 4`), but you can experiment with different settings to balance speed and quality. In general, increasing the threshold results in more aggressive caching, which may improve performance at the expense of image quality. Note that, if you want to change the parameters of the nodes after the first execution, you have to restart the workflow.

> **Note**: Caching and `x_fast` compilation require access to the Pruna Pro version.



## Performance

The node was tested on an NVIDIA L40S GPU. Below, we compare the performance of the base model, with the models 
optimized with Pruna's compilation and caching nodes. We run two types of experiments: one using 50 denoising steps and another 
using 28 steps. We compare the iterations per second (as reported by `ComfyUI`) and the end-to-end time required to generate a single image.


### 50 steps 

![Performance](./images/its_comparison_50.png)
![Performance](./images/end2end_time_comparison_50.png)

**Hyperparameters**: For caching, we use the default hyperparameters, which are `threshold = 0.01` and `max_skip_steps = 4`.

### 28 steps 

![Performance](./images/its_comparison_28.png)
![Performance](./images/end2end_time_comparison_28.png)

**Hyperparameters**: For the SD model, when the number of denoising steps is small, the caching node with the 
default hyperparameters tends to not provide substantial speedups. For that reason, here, only for 
the SD model, we set the threshold to `0.02`. 


## Contact

For **questions, feedback or community discussions**, feel free to join our [Discord](https://discord.com/invite/Tun8YgzxZ9). 

For **bug reports or technical issues**, please open an issue in this repository. 