

def tokens(line):
    if line:
        for token in line.split():
            if token.strip():
                if token[0] == '%':
                    yield 'Nonterminal', token[1:]
                elif token[0] == '$':
                    yield 'Terminal', token[1:]
