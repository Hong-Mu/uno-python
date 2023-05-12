def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = words[0]
    for word in words[1:]:
        if font.size(current_line + ' ' + word)[0] < max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines