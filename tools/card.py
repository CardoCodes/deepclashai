from typing import List, Dict, Union, Optional

class Card:
    """Represents a card with its attributes and statistics.
    
    This class manages card properties including name, type, rarity, and various
    units with their statistics that can change based on card level.
    
    Attributes:
        name: The name of the card.
        type: The type/category of the card.
        rarity: The rarity level of the card.
        units: List of units, where each unit has a name, count, and stats.
        level_stats: Nested list of statistics per card level.
    """

    def __init__(self, name: str) -> None:
        """Initializes a new Card instance.

        Args:
            name: The name of the card.
        """
        self._name = name
        self._type = None
        self._rarity = None
        self._arena = None
        self._evolution = None
        self._units = []  # Replace _stats with _units
        self._level_stats = [[]]  # Index 0 is empty, levels start at 1
    
    @property
    def name(self) -> str:
        """Gets the card name."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Sets the card name.
        
        Args:
            value: The new name for the card.
        
        Raises:
            ValueError: If the name is empty or not a string.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Card name must be a non-empty string")
        self._name = value.strip()
    
    @property
    def type(self) -> str:
        """Gets the card type."""
        return self._type
    
    @type.setter
    def type(self, value: str) -> None:
        """Sets the card type.
        
        Args:
            value: The type/category of the card.
        """
        self._type = value
    
    @property
    def rarity(self) -> str:
        """Gets the card rarity."""
        return self._rarity
    
    @rarity.setter
    def rarity(self, value: str) -> None:
        """Sets the card rarity.
        
        Args:
            value: The rarity level of the card.
        """
        self._rarity = value
    
    @property
    def arena(self) -> str:
        """Gets the card arena."""
        return self._arena
    
    @arena.setter
    def arena(self, value: str) -> None:
        """Sets the card arena.
        
        Args:
            value: The arena level of the card.
        """
        self._arena = value
    
    @property
    def evolution(self) -> str:
        """Gets the card evolution."""
        return self._evolution
    
    @evolution.setter
    def evolution(self, value: str) -> None:
        """Sets the card evolution.
        
        Args:
            value: The evolution level of the card.
        """
        self._evolution = value
    
    @property
    def units(self) -> List[Dict[str, Union[str, int, List]]]:
        """Gets the card's units."""
        return self._units
    
    def add_unit(self, name: str, count: int, stats: Optional[List[Dict[str, Union[int, float, str]]]] = None) -> None:
        """Adds a new unit to the card with optional stats.
        
        Args:
            name: The name of the unit.
            count: The number of this unit.
            stats: Optional list of stats for the unit, where each stat is a dict with 'name' and 'value' keys.
        """
        unit = {
            'name': name,
            'count': count,
            'stats': []
        }
        
        if stats:
            for stat in stats:
                unit['stats'].append({
                    'name': stat['name'],
                    'value': stat['value']
                })
                
        self._units.append(unit)
    
    def set_level_stats(self, level: int, stats: Dict[str, Union[int, float, str]]) -> None:
        """Sets statistics for a specific card level.
        
        Args:
            level: The card level to set statistics for.
            stats: Dictionary of stat names and their values.
        
        Raises:
            ValueError: If level is less than 1.
        """
        if level < 1:
            raise ValueError("Card level must be 1 or greater")
            
        while len(self._level_stats) <= level:
            self._level_stats.append([])
        
        level_stats = []
        for stat_name, stat_value in stats.items():
            level_stats.append({
                'name': stat_name,
                'value': stat_value
            })
        self._level_stats[level] = level_stats
    
    def get_level_stats(self, level: int) -> List[Dict[str, Union[str, float]]]:
        """Gets statistics for a specific card level.
        
        Args:
            level: The card level to get statistics for.
            
        Returns:
            A list of dictionaries containing the statistics for the specified level.
            
        Raises:
            ValueError: If level is less than 1 or greater than maximum level.
        """
        if level < 1 or level >= len(self._level_stats):
            raise ValueError(f"Invalid level: {level}")
        return self._level_stats[level]
    
    def to_dict(self) -> Dict[str, Union[str, List]]:
        """Converts the card object to a dictionary representation.
        
        Returns:
            A dictionary containing the card's data.
        """
        return {
            'name': self._name,
            'type': self._type,
            'rarity': self._rarity,
            'arena': self._arena,
            'evolution': self._evolution,
            'units': self._units,
            'level_stats': self._level_stats[1:]  # Exclude empty level 0
        }
