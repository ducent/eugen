from sure import expect
from eugen.site import Site

class TestSiteData:

  def test_it_should_compile_data_with_success(self):
    site = Site()

    root_definition = {
      '_': [],
      'declarations': [':root'],
      'version': ['1.0.0'],
      'name': ['eugen'],
      'properties': [],
    }

    site.add_result('style.css', [
      root_definition,
      {
        '_': [],
        'declarations': ['.a-block', '.same-block'],
        'block': ['A block with some description'],
        'properties': [],
      },
      {
        '_': [],
        'declarations': ['.another-block'],
        'block': ['Another block here'],
        'properties': [],
      },
      {
        '_': [],
        'declarations': ['.an-element'],
        'element': ['An element'],
        'properties': [],
      },
    ])
  
    expect(site.generated_from).to.equal(['style.css'])
    expect(site.data).to.have.length_of(4)

    site.compile()

    expect(site.groups).to.have.key('block')
    expect(site.groups).to.have.key('element')

    expect(site.groups['block']).to.have.length_of(2)
    expect(site.groups['block'][0]['url']).to.equal('a-block/index.html')
    expect(site.groups['block'][1]['url']).to.equal('another-block/index.html')

    expect(site.groups['element']).to.have.length_of(1)
    expect(site.groups['element'][0]['url']).to.equal('an-element/index.html')
    
    expect(site.root).to.equal(root_definition)
    expect(site.root['url']).to.equal('index.html')