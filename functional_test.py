from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest


class NewVsitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome("chromedriver.exe")

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get("http://localhost:8000")

        # Edith ouviu falar que agora a aplicação online de lista de tarefas
        # aceita definir prioridades nas tarefas do tipo baixa, média e alta
        # Ela decide verificar a homepage

        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')


# Ela percebe que o título da página e o cabeçalho mencionam
# listas de tarefas com prioridade (priority to-do)


# Ela é convidada a inserir um item de tarefa e a prioridade da
# mesma imediatamente


# Ela digita "Comprar anzol" em uma nova caixa de texto
# e assinala prioridade alta no campo de seleção de prioridades


# Quando ela tecla enter, a página é atualizada, e agora
# a página lista "1 - Comprar anzol - prioridade alta"
# como um item em uma lista de tarefas

# Ainda continua havendo uma caixa de texto convidando-a a
# acrescentar outro item. Ela insere "Comprar cola instantâne"
# e assinala prioridade baixa pois ela ainda tem cola suficiente
# por algum tempo


# A página é atualizada novamente e agora mostra os dois
# itens em sua lista e as respectivas prioridades


# Edith se pergunta se o site lembrará de sua lista. Então
# ela nota que o site gerou um URL único para ela -- há um
# pequeno texto explicativo para isso.


# Ela acessa essa URL -- sua lista de tarefas continua lá.

if __name__ == '__main__':
    unittest.main()
