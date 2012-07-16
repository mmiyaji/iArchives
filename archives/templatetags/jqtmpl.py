from django.template import Library, TextNode, TOKEN_BLOCK, TOKEN_VAR

register = Library()

@register.tag
def jqtmpl(parser, token):
    nodes = []
    t = parser.next_token()
    while not (t.token_type == TOKEN_BLOCK and t.contents == "endjqtmpl"):
        if t.token_type == TOKEN_BLOCK:
            nodes.extend(["{%", t.contents, "%}"])
        elif t.token_type == TOKEN_VAR:
            nodes.extend(["{{", t.contents, "}}"])
        else:
            nodes.append(t.contents)
        t = parser.next_token()
    return TextNode(''.join(nodes))
