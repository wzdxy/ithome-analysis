import math
from db import ConnectDb
from output import Output


class IthomeAnalysis:
    def main(self):
        self.clear_old()

        ConnectDb.analysis.insert(self.count_forum_article())
        ConnectDb.analysis.insert(self.count_source_article())
        ConnectDb.analysis.insert(self.count_topic_article())
        ConnectDb.analysis.insert(self.count_editor_article())

        Output().output_to_json()
        return True

    # 新闻来源文章数量
    @staticmethod
    def count_source_article():
        count_data = ConnectDb.article.aggregate([
            {'$match': {'source': {'$ne': 'IT之家'}}},
            {'$group': {'_id': '$source', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 15}
        ])
        return_data = {
            'name': 'source_article_sort',
            'data': {
                'cols': [],
                'counts': []
            }
        }
        for item in count_data:
            return_data['data']['cols'].append(item['_id'])
            return_data['data']['counts'].append(item['count'])
        print('文章来源排名:', return_data['data'])
        return return_data

    # 板块文章数量
    @staticmethod
    def count_forum_article():
        count_data = ConnectDb.article.aggregate([
            {'$group': {'_id': '$forum_id', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ])
        return_data = {
            'name': 'forum_article_sort',
            'data': {
                'cols': [],
                'counts': []
            }
        }
        for item in count_data:
            return_data['data']['cols'].append(item['_id'])
            return_data['data']['counts'].append(item['count'])
        print('板块文章数量:', return_data['data'])
        return return_data

    # 话题文章数量
    @staticmethod
    def count_topic_article():
        count_data = ConnectDb.article.aggregate([
            {'$group': {'_id': '$topic_id', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}

        ])
        return_data = {
            'name': 'topic_article_sort',
            'data': {
                'cols': [],
                'counts': []
            }
        }
        for item in count_data:
            return_data['data']['cols'].append(item['_id'])
            return_data['data']['counts'].append(item['count'])
        print('话题文章数量:', return_data['data'])
        return return_data

    @staticmethod
    def count_editor_article():
        count_data = ConnectDb.article.aggregate([
            # {'$match': {'source': 'IT之家'}},
            {'$group': {'_id': '$editor', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ])
        return_data = {
            'name': 'count_editor_article',
            'data': {
                'cols': [],
                'counts': []
            }
        }
        for item in count_data:
            return_data['data']['cols'].append(item['_id'])
            return_data['data']['counts'].append(item['count'])
        print('编审文章数量:', return_data['data'])
        return return_data

    @staticmethod
    def count_editor_info():
        count_data = ConnectDb.article.aggregate([
            {'$group': {'_id': '$editor', 'count': {'$sum': 1}}},
        ])
        return_data = {
            'name': 'count_editor_base_info',
            'data': {
                'cols': [],
                'counts': []
            }
        }
        for item in count_data:
            return_data['data']['cols'].append(item['_id'])
            return_data['data']['counts'].append(item['count'])
        print('原创文章数量:', return_data['data'])
        return return_data

    @staticmethod
    def clear_old():
        # 注意 不能清空 article 表 (原始数据)
        ConnectDb.analysis.delete_many({})
        print('\n已清空原有统计数据\n')


analysis = IthomeAnalysis()
analysis.main()
exit()
