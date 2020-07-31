import sys
import subprocess
from pathlib import Path
from typing import Optional
from briefcase.cmdline import parse_cmdline
from briefcase.commands import NewCommand
from briefcase.commands.base import BriefcaseCommandError
from briefcase.exceptions import BriefcaseError, NetworkFailure

class NewMilkUICommand(NewCommand):
    def build_app_context(self):
        """
        Ask the user for details about the app to be created.

        :returns: A context dictionary to be used in the cookiecutter project
            template.
        """
        formal_name = self.input_text(
            intro="""
First, we need a formal name for your application. This is the name that will
be displayed to humans whenever the name of the application is displayed. It
can have spaces and punctuation if you like, and any capitalization will be
used as you type it.""",
            variable="formal name",
            default='Hello World',
        )

        # The class name can be completely derived from the formal name.
        class_name = self.make_class_name(formal_name)

        default_app_name = self.make_app_name(formal_name)
        app_name = self.input_text(
            intro="""
Next, we need a name that can serve as a machine-readable Python package name
for your application. This name must be PEP508-compliant - that means the name
may only contain letters, numbers, hypehns and underscores; it can't contain
spaces or punctuation, and it can't start with a hyphen or underscore.

Based on your formal name, we suggest an app name of '{default_app_name}',
but you can use another name if you want.""".format(
                default_app_name=default_app_name
            ),
            variable="app name",
            default=default_app_name,
            validator=self.validate_app_name,
        )

        # The module name can be completely derived from the app name.
        module_name = self.make_module_name(app_name)

        bundle = self.input_text(
            intro="""
Now we need a bundle identifier for your application. App stores need to
protect against having multiple applications with the same name; the bundle
identifier is the namespace they use to identify applications that come from
you. The bundle identifier is usually the domain name of your company or
project, in reverse order.

For example, if you are writing an application for Example Corp, whose website
is example.com, your bundle would be ``com.example``. The bundle will be
combined with your application's machine readable name to form a complete
application identifier (e.g., com.example.{app_name}).""".format(
                app_name=app_name,
            ),
            variable="bundle identifier",
            default='com.example',
            validator=self.validate_bundle,
        )

        description = self.input_text(
            intro="""
Now, we need a one line description for your application.""",
            variable="description",
            default="My first application"
        )

        author = self.input_text(
            intro="""
Who do you want to be credited as the author of this application? This could be
your own name, or the name of your company you work for.""",
            variable="author",
            default="Jane Developer",
        )

        author_email = self.input_text(
            intro="""
What email address should people use to contact the developers of this
application? This might be your own email address, or a generic contact address
you set up specifically for this application.""",
            variable="author's email",
            default=self.make_author_email(author, bundle),
            validator=self.validate_email
        )

        url = self.input_text(
            intro="""
What is the website URL for this application? If you don't have a website set
up yet, you can put in a dummy URL.""",
            variable="application URL",
            default=self.make_project_url(bundle, app_name),
            validator=self.validate_url
        )

        project_license = self.input_select(
            intro="""
What license do you want to use for this project's code?""",
            variable="project license""",
            options=[
                "MIT license",
                "BSD license",
                "ISC license",
                "Apache Software License 2.0",
                "GNU General Public License v3",
                "Not open source"
            ],
        )

        return {
            "formal_name": formal_name,
            "app_name": app_name,
            "class_name": class_name,
            "module_name": module_name,
            "project_name": formal_name,
            "description": description,
            "author": author,
            "author_email": author_email,
            "bundle": bundle,
            "url": url,
            "license": project_license
        }
    def new_app(self, template: Optional[str] = None, **options):
        """
        Ask questions to generate a new application, and generate a stub
        project from the briefcase-template.
        """
        if template is None:
            template = 'https://github.com/Satireven/milkui-template'
        
        if self.input.enabled:
            print()
            print("Let's build a new MilkUI app!")
            print()

        context = self.build_app_context()

        print()
        print("Generating a new application '{formal_name}'".format(
            **context
        ))

        cached_template = self.update_cookiecutter_cache(
            template=template,
            branch='v0.3'
        )

        # Make extra sure we won't clobber an existing application.
        if (self.base_path / context['app_name']).exists():
            print()
            raise BriefcaseCommandError(
                "A directory named '{app_name}' already exists.".format(
                    **context
                )
            )

        try:
            # Unroll the new app template
            self.cookiecutter(
                str(cached_template),
                no_input=True,
                output_dir=str(self.base_path),
                checkout="v0.3",
                extra_context=context
            )
        except subprocess.CalledProcessError:
            # Computer is offline
            # status code == 128 - certificate validation error.
            raise NetworkFailure("clone template repository")

        print("""
Application '{formal_name}' has been generated. To run your application, type:

    cd {app_name}
    milkui dev
""".format(**context))


def main():
    try:
        command, options = parse_cmdline(sys.argv[1:])
        command.parse_config('pyproject.toml')
        if isinstance(command, NewCommand):
            # change template to milkui template
            command = NewMilkUICommand(base_path=Path.cwd())
        command(**options)
        result = 0
    except BriefcaseError as e:
        print(e, file=sys.stdout if e.error_code == 0 else sys.stderr)
        result = e.error_code
    except KeyboardInterrupt:
        print()
        print("Aborted by user.")
        print()
        result = -42

    sys.exit(result)


if __name__ == '__main__':
    main()
