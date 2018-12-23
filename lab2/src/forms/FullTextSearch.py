import npyscreen

class FullTextSearch(npyscreen.ActionFormV2):
    def create(self):
        self.value = None
        self.wgWords = self.add(npyscreen.TitleText, name="Obligatory entry of the words:")
        self.wgWordNotBelong = self.add(npyscreen.TitleText, name="Word is not belong:")
        self.wgResults = self.add(npyscreen.TitleFixedText, name="Results:", value='')

    def beforeEditing(self):
        self.name = "Full text search"
        self.wgWords.value = ''
        self.wgWordNotBelong.value = ''

    def on_ok(self):
        if self.wgWords.value:
            search_results = self.parentApp.database.text_search_by_word(self.wgWords.value)
        else:
            search_results = self.parentApp.database.text_search_by_word_not_belong(self.wgWordNotBelong.value)
        self.wgResults.value = ' '
        for t in search_results:
            self.wgResults.value += '\n' + (str(t) + '\n')

    def on_cancel(self):
        self.parentApp.switchFormPrevious()