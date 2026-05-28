CONSOLE_TOOL_NAMES = (
    'autocaps',
    'autolower',
    'autopassword',
    'autoip',
    'autoconvert',
    'autocolor',
    'autounit',
    'autozip',
    'autotodo',
    'autonote',
)

LAZY_TOOL_NAMES = CONSOLE_TOOL_NAMES + ('autotest',)

CONSOLE_SCRIPT_ENTRY_POINTS = (
    'autotools=autotools.cli:cli',
    *(f'{tool_name}=autotools.cli:{tool_name}' for tool_name in CONSOLE_TOOL_NAMES),
)
