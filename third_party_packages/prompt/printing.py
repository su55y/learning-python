from prompt_toolkit import prompt, print_formatted_text as printft, HTML
from prompt_toolkit.styles import Style

stylesheet_dict = lambda: {"prompt": "#9d0006", "text": "#fb4934 italic bg:#9d0006"}
stylesheet = Style.from_dict(stylesheet_dict())


def wrap_tag(tagname: str, value: str) -> HTML:
    tag = tagname if tagname in stylesheet_dict().keys() else "prompt"
    return HTML(f"<{tag}>{value}</{tag}>")


def use_prompt(prompt_text: str):
    try:
        return prompt(wrap_tag("prompt", prompt_text), style=stylesheet)
    except:
        return ""


if __name__ == "__main__":
    text = use_prompt(">> ")
    printft(wrap_tag("text", text), style=stylesheet)
    printft(HTML("<_ bg='#9d0006' fg='#fb4934'>%s</_>" % text))
