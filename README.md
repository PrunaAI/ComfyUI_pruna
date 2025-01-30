# Pruna AI ComfyUI Integration

A custom node for ComfyUI that smashes models using Pruna. 


## Installation

### Prerequisites
1. Create a new conda environment
2. Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
3. Install latest version of [Pruna](https://docs.pruna.ai/en/latest/setup/pip.html)

*Note*: After installing Pruna, you may see a few warnings related to torchaudio. We ignore them for now, 
since they don't affect our node. We will fix this in the future.

### Steps

1. After installing ComfyUI, go to the `custom_nodes` folder and clone this repository.
2. Launch ComfyUI by running `python main.py` in your terminal, from the ComfyUI directory.
The node should be available in the nodes menu, under `loaders`.


## Example

We wire the `SmashUnet` node as shown in the image below. The first time you run the node, it will take a while to complete.

![Example](./images/example.png)

