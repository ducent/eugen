from arpeggio.peg import PTNodeVisitor

class Visitor(PTNodeVisitor):
  def __init__(self):
    super().__init__(defaults=False)

  def visit_entity(self, node, children):
    return ('entity', node[1].value)

  def visit_empty_comment(self, node, chidren):
    return [('text', '')] # Keep empty lines in comments
  
  def visit_text(self, node, children):
    return ('text', node.value)

  def visit_property_name(self, node, children):
    return node.value

  def visit_property(self, node, children):
    definition = {
      'name': children.property_name[0],
    }

    if children.comment:
      definition.update(children.comment[0])

    return definition

  def visit_declaration(self, node, children):
    return node.value.strip()

  def visit_comment_line(self, node, children):
    return children

  def visit_comment(self, node, children):
    flattened_children = [item for sublist in children for item in sublist]
    definition = { '_': [] }
    current_entity = None

    for t, content in flattened_children:
      if t == 'entity':
        current_entity = content
        definition[current_entity] = []
      else:
        definition[current_entity if current_entity else '_'].append(content)

    return definition

  def visit_definition(self, node, children):
    definition = {
      'declarations': children.declaration,
      'properties': children.property,
    }

    if children.comment:
      definition.update(children.comment[0])
    
    return definition

  def visit_root(self, node, children):
    return children