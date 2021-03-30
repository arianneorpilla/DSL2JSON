# DSL2JSON

<p align="left">
  <img src="https://i.postimg.cc/YCVj78ny/image.png" alt="picture" height=250>
  <img src="https://i.postimg.cc/SNbxgJXH/image.png" alt="picture" height=250>
</p>

**A script for converting DSL format dictionaries compatible with GoldenDict to the Migaku Dictionary format**.
Useful for converting multilingual dictionaries. Written for the language learning community.

## 🛠️ Features
- **Converts DSL format dictionaries to JSON** tested for compatibility with the Migaku Dictionary Add-on for Anki.
- **Parses and sanitizes DSL tags** and replaces them appropriately for readability.
- Dictionary term and definition imports properly.

## 📖 Usage
* In a working directory, <b><a href="https://github.com/lrorpilla/DSL2JSON/blob/main/DSL2JSON.py">download the script</a></b> and execute it with the command below in the same folder with the DSL file to convert as follows with <b><a href="https://www.python.org/">Python</b></a>
```
python3 DSL2JSON.py filename_of_dictionary_to_convert.dsl
```
* The script will output a `DSL2JSON.zip` file that can be imported with the **Install Dictionary From File** option in the Migaku Dictionary Settings menu. For more information, <b><a href="https://www.migaku.io/tools-guides/migaku-dictionary/manual/#installing-dictionaries">see the official guide on the Migaku add-on</a></b>.
* A `DSL2JSON.json` file is also left behind for debugging purposes should any escape character errors with the JSON occur.

## 🚀 Possible Extensions
- Improve script to recognize **altterm, pronunciation, parts of speech and example fields**.
- **Test script for reliability** on multiple dictionaries.
