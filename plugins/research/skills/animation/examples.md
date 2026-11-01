# Examples of diagrams

Figures of Prince, S. J. D. (2023). *Understanding Deep Learning*. The MIT Press. https://udlbook.github.io/udlbook/
Released by the author under the Creative Commons BY-NC-ND 4.0 license: reproduced here unmodified (only rendered from
PDF to PNG), for non-commercial use, with this credit. They are the reference of the style of this skill: open the
matching images before drawing a mechanism, to see how the book draws it.

| File | Chapter | What it shows, and what to take from it |
| ---- | ------- | ---------------------------------------- |
| `examples/TransformerSA1.png` | 12, Transformers | Self-attention as a network: values computed from each input, weighted and summed. |
| `examples/TransformerSA2.png` | 12 | Queries and keys from the inputs, dot products, softmax over columns, attention weights as a brown heat map. |
| `examples/TransformerBlockSA.png` | 12 | **The reference**: self-attention in matrix form. Tensors as grids with their dimensions (D, N), a name and an equation under each, the module in a teal rounded panel, right-angle arrows. |
| `examples/TransformerBlockSAMultiHead.png` | 12 | Multi-head attention: the same block repeated per head, then concatenated. |
| `examples/TransformerBlockSACross.png` | 12 | Cross-attention: queries from one input (N_d tokens), keys and values from the other (N_e); attention matrix N_e × N_d. |
| `examples/TransformerBlock.png` | 12 | A transformer block: attention, residual, layer norm, MLP, as a chain of tensors. |
| `examples/TransformerPE.png` | 12 | Positional encoding as a matrix added to the input. |
| `examples/TransformerVisionTransformer.png` | 12 | Vision transformer: patches, linear projection, tokens. |
| `examples/TransformerSWIN_compressed.png` | 12 | Shifted windows: the image grid and the windows that attend together. |
| `examples/TransformerEncoderDecoder.png` | 12 | Encoder-decoder with cross-attention between the two stacks. |
| `examples/Conv1.png` | 10, Convolutional networks | 1D convolution: inputs as circles, a kernel of weights sliding, outputs. |
| `examples/Conv1DChannels.png` | 10 | Channels: several kernels give several output channels. |
| `examples/Conv2D.png` | 10 | **The reference for grids**: 2D convolution in four panels a) to d), as frames of an animation; the receptive field in grey, the weights Ω, ⊗ and ⊕, the output node highlighted, the rest of the output faded, zero padding at the border. |
| `examples/ConvDown.png`, `examples/ConvUp.png` | 10 | Down- and up-sampling: which inputs feed which output. |
| `examples/ConvTranspose.png` | 10 | Transposed convolution. |
| `examples/ConvNetworkRF.png` | 10 | **The reference for depth**: layers as orange columns of neurons, the receptive field growing layer after layer as a grey wedge, the kernel size Ω ∈ ℝ^{C×K×K} next to it. |
| `examples/ResidualResNet1.png` | 11, Residual networks | Residual blocks: the skip connection drawn as an arrow around the block. |
| `examples/ResidualUNet.png` | 11 | U-Net: encoder and decoder levels, skip connections, sizes of each level. |
| `examples/GraphNodeEdgeAdjacency.png` | 13, Graph networks | A graph, its node features, its adjacency matrix side by side. |
| `examples/GraphAdjacencyMultiply.png` | 13 | Message passing as a product with the adjacency matrix. |
| `examples/GraphGCN.png` | 13 | A graph convolutional layer: aggregation of the neighbours, then update. |
| `examples/GraphReceptiveField.png` | 13 | The receptive field of a node growing with the number of layers. |
