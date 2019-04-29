from sure import expect
from os import path
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

    expect(site.groups).to.have.length_of(7)
    expect(site.groups).to.have.key('name')
    expect(site.groups).to.have.key('version')
    expect(site.groups).to.have.key('properties')
    expect(site.groups).to.have.key('declarations')
    expect(site.groups).to.have.key('index')
    expect(site.groups).to.have.key('block')
    expect(site.groups).to.have.key('element')

    expect(site.groups['block']).to.have.length_of(2)
    expect(site.groups['block'][0]['url']()).to.equal(path.join('a-block', 'index.html'))
    expect(site.groups['block'][0]['url']('block')).to.equal(path.join('block', 'a-block', 'index.html'))
    expect(site.groups['block'][1]['url']()).to.equal(path.join('another-block', 'index.html'))


    expect(site.groups['element']).to.have.length_of(1)
    expect(site.groups['element'][0]['url']()).to.equal(path.join('an-element', 'index.html'))
    expect(site.groups['element'][0]['url']('element')).to.equal(path.join('element', 'an-element', 'index.html'))
    
    expect(site.root).to.equal(root_definition)
    expect(site.root['url']()).to.equal('index.html')