from ..state import MepoState
from ..utilities import mepoconfig


def run(args):
    if args.style:
        style = args.style
    elif mepoconfig.has_option("init", "style"):
        allowed_styles = ["naked", "prefix", "postfix"]
        style = mepoconfig.get("init", "style")
        if style not in allowed_styles:
            raise Exception(
                f"Detected style [{style}] from .mepoconfig is not an allowed style: {allowed_styles}"
            )
        else:
            print(f"Found style [{style}] in .mepoconfig")
    else:
        style = None

    _ = MepoState.initialize(args.registry, style)

    if not style:
        print(f"Initializing mepo using {args.registry}")
    else:
        print(f"Initializing mepo using {args.registry} with {style} style")
