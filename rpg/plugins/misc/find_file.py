from rpg.plugin import Plugin


class FindFilePlugin(Plugin):

    def compiled(self, project_dir, spec, sack):
        for item in list(project_dir.glob('**/*.*')):
            spec.files.append([item.relative_to(project_dir), None, None])
