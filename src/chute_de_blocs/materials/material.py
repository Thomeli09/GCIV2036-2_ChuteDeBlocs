class Material():
    """
    Represent a material and its basic metadata.
    """

    def __init__(self, name: str, material_type: str, color: str) -> None:
        # Metadata attributes
        self.name = name
        self.material_type = material_type
        self.color = color
    
    # Metadata attributes
    @property
    def name(self) -> str:
        """Return the material name."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Set the material name."""
        self._name = name

    @property
    def material_type(self) -> str:
        """Return the material type."""
        return self._material_type

    @material_type.setter
    def material_type(self, material_type: str) -> None:
        """Set the material type."""
        self._material_type = material_type

    @property
    def color(self) -> str:
        """Return the material color."""
        return self._color

    @color.setter
    def color(self, color: str) -> None:
        """Set the material color."""
        self._color = color