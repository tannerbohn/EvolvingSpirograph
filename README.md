# EvolvingSpirograph
Generative art based on spirographs

![sample](https://github.com/tannerbohn/EvolvingSpirograph/blob/main/tests/collage.png)

Run `python3 main.py` to generate samples.
If you look inside `main.py`, you will see that you can ...
   - change the final image size (I recommend keeping it square)
   - change the set of seeds used for generation -- each image will be saved as a separate `.png`
   - change the colour palette
   - change the image save location


If you want to create your own colour palette...
   - `palette.backgroun` and `line_shadow` are exactly what you might expect
   - `palette.line_options` is a list of colour *gradients* (specified by pairs of colours). Be aware of the fact that if you change the number of gradients listed here, it *might* change the final image generated, due to the stochastic nature of the generation process
   - the `use_noise` option specifies whether to add any perlin noise
