from waterbutler.core import metadata


class BaseDataverseMetadata(metadata.BaseMetadata):

    def __init__(self, raw):
        super().__init__(raw)

    @property
    def provider(self):
        return 'dataverse'


class DataverseFileMetadata(BaseDataverseMetadata, metadata.BaseFileMetadata):

    @property
    def file_id(self):
        return str(self.raw['id'])

    @property
    def name(self):
        return self.raw['name']

    @property
    def path(self):
        return self.build_path(self.file_id)

    @property
    def size(self):
        return None

    @property
    def content_type(self):
        return self.raw['contentType']

    @property
    def modified(self):
        return None

    @property
    def extra(self):
        return {
            'fileId': self.file_id
        }


class DataverseDatasetMetadata(BaseDataverseMetadata, metadata.BaseFolderMetadata):

    def __init__(self, raw, name, doi):
        super().__init__(raw)
        self._name = name
        self.doi = doi

        files = self.raw['files']
        self._entries = [DataverseFileMetadata(f['datafile']) for f in files]

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self.build_path(self.doi)

    @property
    def entries(self):
        return self._entries

    def serialized(self):
        if self._entries:
            return [e.serialized() for e in self._entries]
        return super(DataverseDatasetMetadata, self).serialized()