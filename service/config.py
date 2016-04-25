class Base:

    # Environment Settings
    LOGGER_NAME = 'Bytelog'

    # Path Settings
    STATIC_URL_PATH = ''

    # Jinja Settings
    JINJA_AUTO_RELOAD = False
    JINJA_LSTRIP_BLOCKS = True
    JINJA_TRIM_BLOCKS = True

    # Markdown Settings
    MISAKA_EXTENSIONS = (
        'tables',               # PHP-Markdown style tables
        'fenced-code',          # Github Flavor Code Blocks
        'footnotes',            # [^id] ; [id]: http://example.com/
        'strikethrough',        # ~~strikethrough~~
        'underline',            # _underline_
        'highlight',            # ==highlight==
        'quote',                # "" => <q>quote</q>
        'superscript',          # super^script
        'math',                 # TeX $$math$$
        'no-intra-emphasis',    # disables_emphasis_between_words
        'space-headers',        # Requires space after # header
        'math-explicit'         # ???
    )


class Development(Base):

    # Environment Settings
    DEBUG = True
    TESTING = True

    # Path Settings
    STATIC_URL_PATH = '/static'

    # Jinja Settings
    JINJA_AUTO_RELOAD = True


class Production(Base):

    # Environment Settings
    MINIFY_PAGE = True
