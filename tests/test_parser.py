from sure import expect
from eugen.parser import Parser

class TestParser:

  def test_it_should_parse_a_basic_declaration_with_success(self):
    parser = Parser()

    data = parser.parse("""
/**
 * @block
 * This is the block current description.
 * It may spans multiple lines!
 *
 * @category: useless
 * @say_something: Hi!
 */
.a-block,
.same-block {
  background-color: red;
  display: block;
}
""")

    expect(data).to.have.length_of(1)
    
    d = data[0]
    expect(d['block']).to.equal(['This is the block current description.', 'It may spans multiple lines!', ''])
    expect(d['category']).to.equal(['useless'])
    expect(d['say_something']).to.equal(['Hi!'])

    expect(d['declarations']).to.have.length_of(2)
    expect(d['declarations']).to.equal(['.a-block', '.same-block'])

    expect(d['properties']).to.be.empty

  def test_it_should_contains_properties_in_the_declaring_declarations(self):
    parser = Parser()
    data = parser.parse("""
/**
 * @element: An element with properties
 */
.an-element {
  /**
   * Comments can be here too!
   *
   * @prop: And have properties too!
   */
  --font-size: 18px;
  --bg-color: red;

  color: black;
}
""")

    expect(data).to.have.length_of(1)
    
    d = data[0]
    expect(d['element']).to.equal(['An element with properties'])
    expect(d['declarations']).to.equal(['.an-element'])
    expect(d['properties']).to.have.length_of(2)

    p = d['properties'][0]
    expect(p['name']).to.equal('font-size')
    expect(p['_']).to.equal(['Comments can be here too!', ''])
    expect(p['prop']).to.equal(['And have properties too!'])

    p = d['properties'][1]
    expect(p['name']).to.equal('bg-color')
  
  def test_it_should_ignore_raw_comments(self):
    parser = Parser()
    data = parser.parse("""
/**
 * Some comment should be parsed.
 */
:root {

}

/* And some should not */

/*.unused {
  display: block;
}*/

/**
 * Something else here should be parsed.
 */
.something {

}

""")
    
    expect(data).to.have.length_of(2)
    expect(data[0]['_']).to.equal(['Some comment should be parsed.'])
    expect(data[1]['_']).to.equal(['Something else here should be parsed.'])

  def test_it_should_allow_import_rules(self):
    parser = Parser()
    data = parser.parse("""
@import url('https://fonts.googleapis.com/css?family=Open+Sans&display=swap');

/**
 * Some root element!
 */
:root {

}
""")
    
    expect(data[0]['_']).to.equal(['Some root element!'])