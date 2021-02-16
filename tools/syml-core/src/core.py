
class Location:
    
    class Kind(Enum):
        LOCAL_URI = "LOCAL_URI"
        REMOTE_URI = "REMOTE_URI"
    
    uri: str
    kind: Kind

class Resource:
    """
    Represents a SYML resource - not only limited to SYML definitions but also any other related
    files stored locally or available on the remote location and requiring caching for efficient
    workflows
    """
    local: Location
    remote: Location
    sync_time: datetime
    available: bool
    cacheable: bool
    versioned: bool
    version: str
    meta: dict
    

class Workspace:
    """
    Represents a SYML Workspace. 
    
    Workspace consolidates and manages a set of resources that can be used to work with SYML 
    and related entities. 
    
    Contains locations of the SYML schema files and directories, related resources, markdown files,
    and settings for credential stores which can be used by tooling layer to interact with remote
    databases and orchestration systems
    """
    
    class ResourceKind(Enum):
        
        SYML_SCHEMA = "SYML_SCHEMA"
        SYML_SCHEMA_MIGRATION = "SYML_SCHEMA_MIGRATION"
        SYML_SCHEMA_STATISTICAL_REPORT = "SYML_SCHEMA_STATISTICAL_REPORT"

        SYML_MARKDOWN = "SYML_MARKDOWN"
        
        GENERIC = "GENERIC"
        
    resources: Dict[[location, kind], object] = {}
    location: Location
    repository: Location # TODO: optional git repository to keep everything in sync
    
    def register_resource(location: Location, kind: ResourceKind):
        pass
        
        
class Definition:
    """
    Abstracts YAML definitions
    """
    resource: Resource
    body: object # TODO: this should be a loaded yaml
    
    def check_well_formed(kinds=["Schema", "SchemaMigration", "SchemaReport"]) -> bool:
        return (
            body["apiSpec"] == "syml.somebugs.com/v1" and
            body["kind"] in kinds and 
            "meta" in body and
            "spec" in body
        )


class Schema:
    """
    Represents a SYMLSchema 
    """
    definition: Definition

    @classmethod
    def from_definition(definition: Definition) -> Schema:
        
        if not definition.check_well_formed(["Schema"]):
            raise Exception("schema definition is not well formed")
        
        schema = Schema()
        definition = definition
        return schema
    
    def check_well_formed():
        self.definition.body[]

class ResourceLoader:
    """
    SYML loader is responsible for location resolution resource loading
    
    """
    
    def load(location: Location) -> Resource:
        """
        Loads the SYML schema from location without loading any referenced objects
        """
        return Resource()
    

class SchemaMarshaller:
    """
    Marshalls the SYML schema to YAML file or file object
    """
    
    # TODO: clarify streamable interface
    def marshall(schema: SYMLSchema) -> Streamable:
        return {}
    


class MarkdownDocment:
    """
    Abstracts markdown document with the embedded definitions
    """
    resource: Resource
    definitions: Dict[str, Definition]
    

class MarkdownLoader:
    """
    Loads and processes the markdown file and extracts the embedded SYML definitions
    """

    def load(location: Location) -> MarkdownDocment:
        pass


class MarkdownMarshaller:
    """
    Stores the MarkdownDocment into specified location or into the location that is
    defined in the MarkdownDocment resource location
    """
    
    def save(document: MarkdownDocment, location: Location=None):
        pass


class SchemaMigration:
    """
    Abstracts SYML Schema Migration
    """
    definition: Definition
