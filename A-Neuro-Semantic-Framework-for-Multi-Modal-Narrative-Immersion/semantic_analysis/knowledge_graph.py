"""
Knowledge Graph module for semantic analysis.

Provides capabilities to extract entities and relationships from text
and represent them as a knowledge graph structure.
"""

from typing import Dict, List, Any, Optional, Set, Tuple
import re
from dataclasses import dataclass, field


@dataclass
class Entity:
    """Represents an entity in the knowledge graph."""
    id: str
    name: str
    entity_type: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    mentions: int = 1


@dataclass
class Relation:
    """Represents a relationship between entities."""
    source_id: str
    target_id: str
    relation_type: str
    confidence: float = 1.0
    context: str = ""


class KnowledgeGraphBuilder:
    """
    Builds a knowledge graph from narrative text.
    
    Extracts entities (characters, locations, objects) and their relationships
    to create a structured graph representation.
    """
    
    def __init__(self):
        """Initialize the knowledge graph builder."""
        self.entity_patterns = self._initialize_entity_patterns()
        self.relation_patterns = self._initialize_relation_patterns()
    
    def _initialize_entity_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize patterns for entity extraction.
        
        Returns:
            Dictionary of entity type patterns
        """
        return {
            'PERSON': {
                'patterns': [
                    r'\b([A-Z][a-z]+)\b(?:\s+[A-Z][a-z]+)*',  # Capitalized names
                ],
                'indicators': ['Mr.', 'Mrs.', 'Ms.', 'Dr.', 'Professor', 'King', 'Queen', 'Prince', 'Princess'],
                'pronouns': ['he', 'she', 'him', 'her', 'his', 'hers', 'they', 'them']
            },
            'LOCATION': {
                'patterns': [
                    r'(?:in|at|to|from)\s+(?:the\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                ],
                'indicators': ['city', 'town', 'village', 'country', 'kingdom', 'land', 'forest', 'mountain', 'river', 'castle', 'house', 'building'],
                'prepositions': ['in', 'at', 'to', 'from', 'near', 'by', 'through']
            },
            'ORGANIZATION': {
                'patterns': [
                    r'(?:the\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:Company|Corporation|Institute|Academy|Guild|Order)',
                ],
                'indicators': ['company', 'corporation', 'organization', 'guild', 'order', 'academy', 'institute']
            },
            'OBJECT': {
                'patterns': [
                    r'(?:the|a|an)\s+(\w+\s+)?(?:sword|ring|book|key|stone|crown|wand|staff|orb)',
                ],
                'indicators': ['magical', 'ancient', 'mysterious', 'powerful', 'sacred', 'cursed']
            },
            'EVENT': {
                'patterns': [
                    r'(?:the|a)\s+(\w+\s+)?(?:war|battle|ceremony|festival|journey|quest|adventure)',
                ],
                'indicators': ['great', 'final', 'first', 'last', 'ancient']
            }
        }
    
    def _initialize_relation_patterns(self) -> Dict[str, List[str]]:
        """
        Initialize patterns for relationship extraction.
        
        Returns:
            Dictionary of relation type patterns
        """
        return {
            'FAMILY': [
                r'(\w+)(?:\'s)?\s+(?:father|mother|son|daughter|brother|sister|parent|child)',
                r'(\w+)\s+(?:is|was)\s+(?:the\s+)?(?:father|mother|son|daughter|brother|sister)\s+of\s+(\w+)'
            ],
            'FRIENDSHIP': [
                r'(\w+)\s+(?:and|with)\s+(\w+)\s+(?:are|were)\s+friends',
                r'(\w+)(?:\'s)?\s+(?:friend|companion|ally)'
            ],
            'ROMANTIC': [
                r'(\w+)\s+(?:loves?|loved)\s+(\w+)',
                r'(\w+)\s+(?:and|with)\s+(\w+)\s+(?:married|engaged|together)'
            ],
            'ANTAGONISTIC': [
                r'(\w+)\s+(?:hates?|hated|fought|fights?)\s+(\w+)',
                r'(\w+)(?:\'s)?\s+(?:enemy|rival|opponent|adversary)'
            ],
            'LOCATED_IN': [
                r'(\w+)\s+(?:is|was|lived?|lives?)\s+(?:in|at)\s+(?:the\s+)?(\w+)',
                r'(\w+)\s+(?:came|comes?|went|goes?)\s+(?:to|from)\s+(?:the\s+)?(\w+)'
            ],
            'OWNS': [
                r'(\w+)(?:\'s)?\s+(\w+)',
                r'(\w+)\s+(?:owns?|owned|has|had|possessed?)\s+(?:the\s+)?(\w+)'
            ],
            'MENTOR': [
                r'(\w+)\s+(?:taught|teaches?|trained|trains?)\s+(\w+)',
                r'(\w+)(?:\'s)?\s+(?:mentor|teacher|master|student|apprentice)'
            ]
        }
    
    def build(self, text: str) -> Dict[str, Any]:
        """
        Build a knowledge graph from the input text.
        
        Args:
            text: Input narrative text
            
        Returns:
            Knowledge graph structure with entities and relations
        """
        # Extract entities
        entities = self.extract_entities(text)
        
        # Extract relations
        relations = self.extract_relations(text, entities)
        
        # Build graph structure
        graph = self._build_graph_structure(entities, relations)
        
        # Generate statistics
        stats = self._calculate_statistics(entities, relations)
        
        return {
            'entities': [self._entity_to_dict(e) for e in entities.values()],
            'relations': [self._relation_to_dict(r) for r in relations],
            'graph': graph,
            'statistics': stats
        }
    
    def extract_entities(self, text: str) -> Dict[str, Entity]:
        """
        Extract entities from text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary mapping entity IDs to Entity objects
        """
        entities: Dict[str, Entity] = {}
        entity_counter = 0
        
        for entity_type, type_info in self.entity_patterns.items():
            for pattern in type_info['patterns']:
                matches = re.finditer(pattern, text)
                for match in matches:
                    name = match.group(1) if match.groups() else match.group()
                    name = name.strip()
                    
                    # Skip common words and short names
                    if self._should_skip_entity(name, entity_type):
                        continue
                    
                    # Check if entity already exists
                    existing_id = self._find_existing_entity(entities, name)
                    if existing_id:
                        entities[existing_id].mentions += 1
                    else:
                        entity_id = f"E{entity_counter}"
                        entities[entity_id] = Entity(
                            id=entity_id,
                            name=name,
                            entity_type=entity_type,
                            attributes={'first_mention_pos': match.start()}
                        )
                        entity_counter += 1
        
        return entities
    
    def _should_skip_entity(self, name: str, entity_type: str) -> bool:
        """Check if an entity should be skipped."""
        # Skip very short names
        if len(name) < 2:
            return True
        
        # Skip common words that get falsely detected
        skip_words = {
            'The', 'This', 'That', 'These', 'Those', 'What', 'When', 'Where',
            'Who', 'How', 'Why', 'There', 'Here', 'Now', 'Then', 'But', 'And',
            'Once', 'Upon', 'Time', 'Day', 'One', 'She', 'He', 'It', 'They'
        }
        
        if name in skip_words:
            return True
        
        return False
    
    def _find_existing_entity(self, entities: Dict[str, Entity], name: str) -> Optional[str]:
        """Find an existing entity with the same name."""
        for entity_id, entity in entities.items():
            if entity.name.lower() == name.lower():
                return entity_id
        return None
    
    def extract_relations(
        self, 
        text: str, 
        entities: Dict[str, Entity]
    ) -> List[Relation]:
        """
        Extract relations between entities.
        
        Args:
            text: Input text
            entities: Dictionary of extracted entities
            
        Returns:
            List of Relation objects
        """
        relations: List[Relation] = []
        entity_names = {e.name.lower(): e.id for e in entities.values()}
        
        for relation_type, patterns in self.relation_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    groups = match.groups()
                    if len(groups) >= 2:
                        source_name = groups[0].strip().lower()
                        target_name = groups[1].strip().lower()
                        
                        source_id = entity_names.get(source_name)
                        target_id = entity_names.get(target_name)
                        
                        if source_id and target_id and source_id != target_id:
                            relation = Relation(
                                source_id=source_id,
                                target_id=target_id,
                                relation_type=relation_type,
                                context=match.group()[:100]
                            )
                            relations.append(relation)
        
        return relations
    
    def _build_graph_structure(
        self, 
        entities: Dict[str, Entity], 
        relations: List[Relation]
    ) -> Dict[str, Any]:
        """
        Build a graph structure for visualization.
        
        Args:
            entities: Dictionary of entities
            relations: List of relations
            
        Returns:
            Graph structure with nodes and edges
        """
        nodes = []
        for entity_id, entity in entities.items():
            nodes.append({
                'id': entity_id,
                'label': entity.name,
                'type': entity.entity_type,
                'size': entity.mentions
            })
        
        edges = []
        for relation in relations:
            edges.append({
                'source': relation.source_id,
                'target': relation.target_id,
                'type': relation.relation_type,
                'label': relation.relation_type.replace('_', ' ').title()
            })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'node_count': len(nodes),
            'edge_count': len(edges)
        }
    
    def _calculate_statistics(
        self, 
        entities: Dict[str, Entity], 
        relations: List[Relation]
    ) -> Dict[str, Any]:
        """
        Calculate graph statistics.
        
        Args:
            entities: Dictionary of entities
            relations: List of relations
            
        Returns:
            Statistics dictionary
        """
        # Count entities by type
        entity_types: Dict[str, int] = {}
        for entity in entities.values():
            entity_types[entity.entity_type] = entity_types.get(entity.entity_type, 0) + 1
        
        # Count relations by type
        relation_types: Dict[str, int] = {}
        for relation in relations:
            relation_types[relation.relation_type] = relation_types.get(relation.relation_type, 0) + 1
        
        # Find most mentioned entities
        sorted_entities = sorted(entities.values(), key=lambda x: x.mentions, reverse=True)
        top_entities = [{'name': e.name, 'mentions': e.mentions} for e in sorted_entities[:5]]
        
        return {
            'total_entities': len(entities),
            'total_relations': len(relations),
            'entity_types': entity_types,
            'relation_types': relation_types,
            'top_entities': top_entities,
            # Graph density for directed graph: edges / (nodes * (nodes - 1))
            'graph_density': len(relations) / (len(entities) * (len(entities) - 1)) if len(entities) > 1 else 0,
            'is_directed': True  # Mark as directed graph
        }
    
    def _entity_to_dict(self, entity: Entity) -> Dict[str, Any]:
        """Convert Entity to dictionary."""
        return {
            'id': entity.id,
            'name': entity.name,
            'type': entity.entity_type,
            'mentions': entity.mentions,
            'attributes': entity.attributes
        }
    
    def _relation_to_dict(self, relation: Relation) -> Dict[str, Any]:
        """Convert Relation to dictionary."""
        return {
            'source': relation.source_id,
            'target': relation.target_id,
            'type': relation.relation_type,
            'confidence': relation.confidence,
            'context': relation.context
        }
    
    def _escape_cypher_string(self, value: str) -> str:
        """
        Escape a string for safe use in Cypher queries.
        
        Args:
            value: String to escape
            
        Returns:
            Escaped string safe for Cypher queries
        """
        # Escape backslashes first, then single quotes
        escaped = value.replace('\\', '\\\\').replace("'", "\\'")
        # Remove any potentially dangerous characters
        escaped = ''.join(c for c in escaped if c.isprintable())
        return escaped
    
    def to_cypher(self, graph: Dict[str, Any]) -> str:
        """
        Convert graph to Cypher query for Neo4j.
        
        Args:
            graph: Graph structure
            
        Returns:
            Cypher query string
        """
        queries = []
        
        # Create nodes with escaped values
        for node in graph['nodes']:
            escaped_id = self._escape_cypher_string(node['id'])
            escaped_label = self._escape_cypher_string(node['label'])
            escaped_type = self._escape_cypher_string(node['type'])
            query = f"CREATE (n:{escaped_type} {{id: '{escaped_id}', name: '{escaped_label}', mentions: {node['size']}}})"
            queries.append(query)
        
        # Create relationships with escaped values
        for edge in graph['edges']:
            escaped_source = self._escape_cypher_string(edge['source'])
            escaped_target = self._escape_cypher_string(edge['target'])
            escaped_rel_type = self._escape_cypher_string(edge['type'])
            query = f"MATCH (a {{id: '{escaped_source}'}}), (b {{id: '{escaped_target}'}}) CREATE (a)-[:{escaped_rel_type}]->(b)"
            queries.append(query)
        
        return ";\n".join(queries)
    
    def to_graphml(self, graph: Dict[str, Any]) -> str:
        """
        Convert graph to GraphML format.
        
        Args:
            graph: Graph structure
            
        Returns:
            GraphML XML string
        """
        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
            '  <key id="label" for="node" attr.name="label" attr.type="string"/>',
            '  <key id="type" for="node" attr.name="type" attr.type="string"/>',
            '  <key id="reltype" for="edge" attr.name="type" attr.type="string"/>',
            '  <graph id="G" edgedefault="directed">'
        ]
        
        # Add nodes
        for node in graph['nodes']:
            xml_parts.append(f'    <node id="{node["id"]}">')
            xml_parts.append(f'      <data key="label">{node["label"]}</data>')
            xml_parts.append(f'      <data key="type">{node["type"]}</data>')
            xml_parts.append('    </node>')
        
        # Add edges
        for i, edge in enumerate(graph['edges']):
            xml_parts.append(f'    <edge id="e{i}" source="{edge["source"]}" target="{edge["target"]}">')
            xml_parts.append(f'      <data key="reltype">{edge["type"]}</data>')
            xml_parts.append('    </edge>')
        
        xml_parts.append('  </graph>')
        xml_parts.append('</graphml>')
        
        return '\n'.join(xml_parts)
