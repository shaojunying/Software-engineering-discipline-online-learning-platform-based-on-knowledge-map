class helper:
    @staticmethod
    def read_file(path):
        """
        读取path下的文件，并逐行返回
        :param path:
        :return:
        """
        with open(path, encoding="utf-8") as f:
            while True:
                line = f.readline().strip()
                if not line:
                    break
                yield line
