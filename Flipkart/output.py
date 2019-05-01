import os
import time
import xlwt


class Output(object):
    def __init__(self):
        self.workbook = xlwt.Workbook(encoding='UTF-8')
        # 新增一个表单
        self.sheet = self.workbook.add_sheet("comments")
        self.sheet.col(0).width = 256 * 10
        self.sheet.col(1).width = 256 * 20
        self.sheet.col(2).width = 256 * 20
        self.sheet.col(3).width = 256 * 20
        self.sheet.col(4).width = 256 * 30
        self.sheet.col(5).width = 256 * 50
        self.sheet.write(0, 0, '评分数')
        self.sheet.write(0, 1, '购买者')
        self.sheet.write(0, 2, '时间')
        self.sheet.write(0, 3, '城市')
        self.sheet.write(0, 4, '标题')
        self.sheet.write(0, 5, '内容')
        self.sheet.write(0, 6, '内容翻译')

    def set_sheet_style(self, workbook):
        font = xlwt.Font()
        font.bold = True

        #设置表格的边框
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN

        # 设置居中
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
        alignment.vert = xlwt.Alignment.VERT_TOP  # 垂直方向


    def add_comments(self, row, comments_list):
        for index in range(len(comments_list)):
            self.sheet.write(row + index +1, 0, comments_list[index].get("star"))
            self.sheet.write(row + index +1, 1, comments_list[index].get("name"))
            self.sheet.write(row + index +1, 2, comments_list[index].get("time"))
            self.sheet.write(row + index +1, 3, comments_list[index].get("city"))
            self.sheet.write(row + index +1, 4, comments_list[index].get("title"))
            self.sheet.write(row + index +1, 5, comments_list[index].get("comment"))
            self.sheet.write(row + index +1, 6, comments_list[index].get("trans"))

    def save_comments(self):
        file_name = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
        save_dir = 'comments' + os.path.sep + file_name + ".xls"
        self.workbook.save(save_dir)
