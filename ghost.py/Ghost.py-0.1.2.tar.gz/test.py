import logging
from ghost import Ghost
import xml.etree.ElementTree as et


agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'
ghost = Ghost(wait_timeout=30, user_agent=agent, log_level=logging.CRITICAL, display=True)


def ask(question):
    api_url = 'http://products.wolframalpha.com/api/explorer.html'
    ghost.open(api_url)

    form_id = 'form#apiex'

    # Fill the input
    ghost.set_field_value('%s input[type=text]' % form_id, question)

    # Submit the form
    ghost.click('%s input[type=submit]' % form_id)

    # Descend to frame
    ghost.frame('results')

    # Wait for result
    ghost.wait_for_text('xml version')

    # Do stuff with result (frame content)
    text = ghost.main_frame.toPlainText()
    xml = et.fromstring(text)  # Parse xml from result
    result = ' '.join(
        [node.text for node in  xml.findall('./pod/subpod/plaintext')]
    )

    # Acsend back to root frame
    ghost.frame()

    return result



print ask('what is the height of everest?')
print ask('what is the height of Mont Blanc?')

# Display for 5 more seconds
ghost.sleep(5)
