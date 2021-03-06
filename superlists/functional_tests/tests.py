import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select

MAX_WAIT = 10


class NewVsitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome("C:\\Users\\letic\\PycharmProjects\\ProblemUnidade2\\superlists"
                                        "\\functional_tests\\chromedriver.exe")

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)

        # Edith ouviu falar que agora a aplicação online de lista de tarefas
        # aceita definir prioridades nas tarefas do tipo baixa, média e alta
        # Ela decide verificar a homepage

        # Ela percebe que o título da página e o cabeçalho mencionam
        # listas de tarefas com prioridade (priority to-do)

        self.assertIn('Priority To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Priority To-Do', header_text)

        # Ela é convidada a inserir um item de tarefa e a prioridade da
        # mesma imediatamente

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Ela digita "Comprar anzol" em uma nova caixa de texto
        # e assinala prioridade alta no campo de seleção de prioridades

        inputbox.send_keys('Comprar anzol')
        select = Select(self.browser.find_element_by_id('input01'))
        select.select_by_visible_text('Alta')

        # Quando ela tecla enter, a página é atualizada, e agora
        # a página lista "1 - Comprar anzol - prioridade alta"
        # como um item em uma lista de tarefas

        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Comprar anzol - Prioridade Alta')

        # Ainda continua havendo uma caixa de texto convidando-a a
        # acrescentar outro item. Ela insere "Comprar cola instantâne"
        # e assinala prioridade baixa pois ela ainda tem cola suficiente
        # por algum tempo

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Comprar cola instantânea")
        select = Select(self.browser.find_element_by_id('input01'))
        select.select_by_visible_text('Baixa')
        inputbox.send_keys(Keys.ENTER)

        # A página é atualizada novamente e agora mostra os dois
        # itens em sua lista e as respectivas prioridades

        self.wait_for_row_in_list_table('1: Comprar anzol - Prioridade Alta')
        self.wait_for_row_in_list_table('2: Comprar cola instantânea - Prioridade Baixa')

# Edith se pergunta se o site lembrará de sua lista. Então
# ela nota que o site gerou um URL único para ela -- há um
# pequeno texto explicativo para isso.
    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Comprar anzol')
        select = Select(self.browser.find_element_by_id('input01'))
        select.select_by_visible_text('Alta')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Comprar anzol - Prioridade Alta')

        # Ela percebe que sua lista te um URL único
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

# Ela acessa essa URL -- sua lista de tarefas continua lá.
        self.browser.quit()
        self.browser = webdriver.Chrome("C:\\Users\\letic\\PycharmProjects\\ProblemUnidade2\\superlists"
                                        "\\functional_tests\\chromedriver.exe")

        self.assertRegex(edith_list_url, '/lists/.+')

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Comprar anzol - Prioridade Alta', page_text)
        self.assertIn('Comprar cola instantânea - Prioridade Baixa', page_text)