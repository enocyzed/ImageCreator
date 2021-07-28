# ImageCreator

A python package that lets you create image templates. It can be used with self coded plugins to produce dynamically changing images with the same template.

## Installation
### Download
1. __Download__ the repository as a Zip-file
2. __Unzip__ the repository to a desired directory
3. *You may need to rename the repository to `ImageCreator`.*

### PIP
*pip package is coming soon!*

## Usage
0. *using VS Code as text editor for this is recommended*

1. Create this `run.py` file (within the directory where you saved the ImageCreator if not installed with PIP):
    ```python
    # run.py
    import ImageCreator

    ImageCreator.start()
    ```
2. Run the `run.py` file. It will create a structure like this when first executed:
    ```css
    root
    ├ (ImageCreator)
    ├ Assets
    |  ├ fonts
    |  |  └ _fonts.py
    |  ├ images
    |  └ plugins
    ├ CreateConfigurations
    |  └ created_images
    └ run.py
    ```

3. Create a template with the template editor GUI
<br></br>

## Using the template editor GUI

1. __Select file button__:  
Select a configuration file in the file dialog that you want to edit.
2. __Stay on top checkbox__:  
Make the window stay on top of all other windows (useful when you are editing a configuration file).
3. __Auto refresh checkbox__:
Make the image refresh automatically to directly see your changes.
4. __Refresh Button__:  
Refresh the image manually (recommended for slower PCs).
5. __Add File/Add Overlay Button__
When no file is selected, you can click on the button to create and save a new configuration file.  
When there is a file selected, you can add overlays to an image object with:  `a: OVERLAY_KEYWORD`  
__Overlay keywords:__  
`image` or `img` to add an image overlay  
`text` or `txt` to add a text overlay  
`multiline_text` or `multiline` or `multi` or `mtxt` to add a multiline text overlay  
  
When you have a configuration file selected or created, you can open it in VS Code and edit it. When you activate Auto Save in VS Code and Auto Refresh in the GUI, you can see what your changes did directly.

## Additional Features
### __Fonts__:
You can put fonts in `.ttf` or `.otf` format inside the `root/Assets/fonts` directory so that you can use them.
### __Images__:
You can put images inside the `root/Assets/images` directory so that you can use them as an overlay, or the background.
### __Plugins__:
Plugins can be used to add anything (for example text) to the image at the time of its creation. Add them to your configuration file like this:
```yaml
# your_configuration.yaml
...
message:
    plugin: YOUR_PLUGIN
    kwargs:
        KEYWORD: ARGUMENT

... OR ...

message: {plugin: YOUR_PLUGIN, kwargs: {KEYWORD: ARGUMENT}}
```
They can be used with keyword arguments if needed, and even get their keyword arguments trough another plugin.  
Plugins need to be in the `root/Assets/plugins` directory and need to have a run method, that returns the desired output.


```python
# example_plugin.py
import time

def run():
    time_now = time.ctime()
    return time_now
```
*Callable with:* `{plugin: example_plugin}`  
*Example Output*: `Tue Jun  8 13:32:09 2021`

<br><br/>
```python
# example_plugin2.py

def run(name):
    sentence = f"Hello {name}, have a great day!"
    return sentence
```
*Callable with:* `{plugin: example_plugin2, kwargs:{name: Peter Griffin}}`  
*Example Output*: `Hello Peter Griffin, have a great day!`

<br><br/>

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Notes
This is my very first attempt to publish something to github, so I am still learning and always open for feedback. If you think there is something I could do better or if you want to cooperate, feel free to contact me at: enocyzed@gmail.com

## License
[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)
