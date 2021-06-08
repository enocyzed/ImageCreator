# ImageCreator

A python package that lets you create image templates. It can be used with self coded plugins to make different images with the same template.

## Installation
---
### Download
1. __Download__ the repository as a Zip-file
2. __Unzip__ the repository to a desired directory
3. *You may need to rename the repository to `ImageCreator`.*

### PIP
*pip package is coming soon!*

## Usage
---
0. *using an IDE like VS Code for this is recommended*

1. Create this `run.py` file within the directory where you saved the ImageCreator:
    ```python
    # run.py
    import ImageCreator

    ImageCreator.create_template()
    ImageCreator.create_on_pressed()
    ```
2. Run the `run.py` file. It will create a structure like this:
    ```css
    root
    ├ ImageCreator
    ├ Assets
    |  ├ fonts
    |  |  └ _fonts.py
    |  ├ images
    |  └ plugins
    ├ CreateConfigurations
    |  └ created_images
    └ run.py
    ```

3. Create a template with the desired ...
    - __overlays__
    - __name__
    - __format__ (yaml, json) -> *yaml is recommended*
    - __flowstyle__ (none, default, full) -> *default is recommended*

4. Open the created file from `root/CreateConfigurations` and select it in the command prompt.

5. Press enter and open the __created image__ from `root/CreateConfigurations/created_images`

6. Modify your __configuration file__ and press enter when you want to see what you did.

## Additional Features
---
### __Fonts__:
You can put fonts in `.ttf` or `.otf` format inside the `root/Assets/fonts` directory so that you can use them.
### __Images__:
You can put images inside the `root/Assets/images` directory so that you can use them as an overlay, or the background.
### __Plugins__:
Plugins can be used to add anything (for example text) to the image at the time of its creation. Add them to your configuration file like this:
```yaml
# your_configuration.yaml
...
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
*Callable with:* `{"plugin": "example_plugin"}`  
*Example Output*: `Tue Jun  8 13:32:09 2021`


<br/>

```python
# example_plugin2.py

def run(name):
    sentence = f"Hello {name}, have a great day!"
    return sentence
```
*Callable with:* `{"plugin": "example_plugin2", "kwargs":{"name": "Peter Griffin"}}`  
*Example Output*: `Hello Peter Griffin, have a great day!`  
.  

*(Quotation marks can be left out when using the .yaml format)*
## Contributing
---
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Notes
---
This is my very first attempt to publish something to github, so I am still learning and always open for feedback, so if you think there is something I could do better or want to cooperate, feel free to contact me at: enocyzed@gmail.com

## License
---
[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)
