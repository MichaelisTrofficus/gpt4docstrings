from typing import List

from redbaron import RedBaron

from gpt4docstrings import config


class GPT4Docstrings:

    def __init__(self, paths, conf=None, excluded=None):
        pass

    def get_filenames_from_paths(self):
        """Find all files to measure for docstring coverage."""
        filenames = []
        for path in self.paths:
            if os.path.isfile(path):
                if not path.endswith(".py"):
                    msg = (
                        "E: Invalid file '{}'. Unable interrogate non-Python "
                        "files.".format(path)
                    )
                    click.echo(msg, err=True)
                    return sys.exit(1)
                filenames.append(path)
                continue
            for root, dirs, fs in os.walk(path):
                full_paths = [os.path.join(root, f) for f in fs]
                filenames.extend(self._filter_files(full_paths))

        if not filenames:
            p = ", ".join(self.paths)
            msg = "E: No Python files found to interrogate in '{}'.".format(p)
            click.echo(msg, err=True)
            return sys.exit(1)

        self.common_base = utils.get_common_base(filenames)
        return filenames



    def _get_list_of_nodes(self):
        pass

    def _generate_file_docstrings(self, filename: str):
        """
        Generates docstrings for a file.

        Args:
            filename: The filename to be potentially documented

        Returns:
            A list of `DocsNode`
        """
        source = RedBaron(open(filename, "r", encoding="utf-8").read())

        for node in source.find_all("class"):
            node_source_code = node.dumps()
            # Check if class is complete (just ignore for now __init__)
            # TODO: Call OpenAI

        for node in source.find_all("def"):
            if not node.value[0].type == "string":
                # Generate docstrings here!
                docstring = "This is a generated docstring!!"
                if node.next and node.next.type == "comment":
                    node.next.insert_after(f'"""\n{docstring}\n"""')
                else:
                    node.value.insert(0, f'"""\n{docstring}\n"""')

        with open(filename, "w", encoding="utf-8") as file:
            file.write(source.dumps())

        # tree = ast.parse(open(filename, encoding="utf-8").read())
        # # transformer = DocsTransformer(filename=filename, source=tree, config=self.config)
        # # new_tree = transformer.visit(tree)
        # transformer = DocstringWriter()
        # new_tree = transformer.visit(tree)
        # ast.fix_missing_locations(new_tree)
        # src = ast.unparse(new_tree)
        # with open(filename, "w") as f:
        #     f.write(src)

        #
        #
        #
        # filtered_nodes = self._filter_nodes(visitor.nodes)
        # if len(filtered_nodes) == 0:
        #     return
        #
        # # First of all, just take those nodes with source code (containing lineno, etc.)
        # filtered_nodes = [n for n in filtered_nodes if n.source_code]
        #
        # if self.config.ignore_nested_functions:
        #     filtered_nodes = [
        #         n for n in filtered_nodes if not n.is_nested_func
        #     ]
        # if self.config.ignore_nested_classes:
        #     filtered_nodes = self._filter_inner_nested(filtered_nodes)
        #
        # return filtered_nodes

    def _generate_docstrings(self, filenames: List[str]):
        """
        Traverses the filenames and generate docstrings for undocumented classes / functions
        inside each file.

        Args:
            filenames: A list of files to be potentially documented.
        """
        for filename in filenames:
            self._generate_file_docstrings(filename)
            # TODO: We should call the LLM API and write the docstrings for whatever function we want
            print(1)

    def generate_docstrings(self):
        """
        Generates docstrings for undocumented classes / functions
        """
        filenames = self.get_filenames_from_paths()
        return self._generate_docstrings(filenames)
