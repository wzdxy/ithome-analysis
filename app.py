import math
from db import ConnectDb
from output import Output


class IthomeAnalysis:
    def main(self):
        self.clear_old()

        ConnectDb.analysis.insert(self.base_info())
        ConnectDb.analysis.insert(self.count_forum_article())
        ConnectDb.analysis.insert(self.count_source_article())
        ConnectDb.analysis.insert(self.count_topic_article())
        ConnectDb.analysis.insert(self.count_editor_article())
        ConnectDb.analysis.insert(self.count_editor_original_radio())
        ConnectDb.analysis.insert(self.editor_grade_order())
        ConnectDb.analysis.insert(self.article_grade_order())
        ConnectDb.analysis.insert(self.article_comment_count_order())

        Output().output_to_json()
        return True

    @staticmethod
    def base_info():
        return_data = {
            'name': 'base_info',
            'data': {}
        }

        # 评论总数
        return_data['data']['comment_count'] = list(ConnectDb.article.aggregate([
            {'$group': {'_id': '$tm_year', 'sum': {'$sum': '$comment_count'}}},
            {'$sort': {'_id': 1}}
        ]))

        # 小编列表
        return_data['data']['editor_list'] = list(ConnectDb.article.aggregate([
            {'$group': {'_id': '$editor'}},
        ]))

        # 小编总数
        return_data['data']['editor_count'] = len(return_data['data']['editor_list'])

        print('基本信息:', return_data['data'])
        return return_data

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

    # 小编文章数量
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

    # 小编的原创文章比例
    @staticmethod
    def count_editor_original_radio():
        count_data = ConnectDb.article.aggregate([
            {
                '$group': {
                    '_id': '$editor',
                    'count': {'$sum': 1},
                    'count_original': {'$sum': {'$cond': [{'$eq': ['$source', 'IT之家']}, 1, 0]}}
                },
            }, {
                '$match': {
                    'count': {'$gt': 100}
                }
            }, {
                '$project': {
                    'original_ratio': {'$divide': ['$count_original', '$count']},
                    'count':'$count',
                    'count_original':'$count_original',
                }
            }, {
                '$sort': {
                    'original_ratio': -1,
                    'count': -1
                }
            }])
        return_data = {
            'name': 'count_editor_original_radio',
            'data': {
                'cols': [],
                'counts': [],
                'count_original': [],
                'original_ratio': [],
            }
        }
        for item in count_data:
            return_data['data']['cols'].append(item['_id'])
            return_data['data']['counts'].append(item['count'])
            return_data['data']['count_original'].append(item['count_original'])
            return_data['data']['original_ratio'].append(item['original_ratio'])
        print('原创文章数量:', return_data['data'])
        return return_data

    # 小编评分排行
    @staticmethod
    def editor_grade_order():
        grade_data = ConnectDb.article.aggregate([
            {
                '$match': {
                    'grade': {'$exists': True}
                },
            }, {
                '$group': {
                    '_id': '$editor',
                    'grade_sum': {'$sum': '$grade'},
                    'count': {'$sum': 1}
                }
            }, {
                '$match': {
                    'count': {'$gt': 20}
                }
            }, {
                '$project': {
                    'grade_avg': {'$divide': ['$grade_sum', '$count']},
                    'grade_sum': '$grade_sum',
                    'count': '$count'
                }
            }, {
                '$sort': {
                    'grade_avg': -1,
                    'count': -1
                },
            }, {
                '$limit': 15
            }])
        return_data = {
            'name': 'editor_grade_order',
            'data': {
                'cols': [],
                'grade_avg': [],
                'grade_sum': [],
                'counts': [],
            }
        }
        for item in grade_data:
            return_data['data']['cols'].append(item['_id'])
            return_data['data']['grade_avg'].append(item['grade_avg'])
            return_data['data']['grade_sum'].append(item['grade_sum'])
            return_data['data']['counts'].append(item['count'])
        print('小编评分排行:', return_data['data'])
        return return_data

    # 文章评分排行
    @staticmethod
    def article_grade_order():
        grade_data = ConnectDb.article.aggregate([
            {
                '$match': {
                    'grade': {'$exists': True},
                },
            }, {
                '$sort': {
                    'grade': -1,
                    'grade_people_count': -1
                },
            }, {
                '$limit': 25
            }
        ])
        return_data = {
            'name': 'article_grade_order',
            'data': {
                'cols': [],
                'grade': [],
                'grade_people_count': [],
                'title': [],
                'article_url': [],
                'source': [],
                'editor': [],
            }
        }
        for item in grade_data:
            return_data['data']['cols'].append(item['article_id'])
            return_data['data']['grade'].append(item['grade'])
            return_data['data']['grade_people_count'].append(item['grade_people_count'])
            return_data['data']['title'].append(item['title'])
            return_data['data']['article_url'].append(item['article_url'])
            return_data['data']['source'].append(item['source'])
            return_data['data']['editor'].append(item['editor'])

        print('文章评分排行:', return_data['data'])
        return return_data

    # 文章评分排行
    @staticmethod
    def article_comment_count_order():
        grade_data = ConnectDb.article.aggregate([
            {
                '$sort': {
                    'comment_count': -1,
                },
            }, {
                '$limit': 25
            }
        ])
        return_data = {
            'name': 'article_comment_count_order',
            'data': {
                'cols': [],
                'grade': [],
                'comment_count': [],
                'title': [],
                'article_url': [],
                'source': [],
                'editor': [],
            }
        }
        for item in grade_data:
            return_data['data']['cols'].append(item['article_id'])
            if 'grade' in item :
                return_data['data']['grade'].append(item['grade'])
            else:
                return_data['data']['grade'].append(None)
            return_data['data']['comment_count'].append(item['comment_count'])
            return_data['data']['title'].append(item['title'])
            return_data['data']['article_url'].append(item['article_url'])
            return_data['data']['source'].append(item['source'])
            return_data['data']['editor'].append(item['editor'])

        print('文章评论数排行:', return_data['data'])
        return return_data

    @staticmethod
    def clear_old():
        # 注意 不能清空 article 表 (原始数据)
        ConnectDb.analysis.delete_many({})
        print('\n已清空原有统计数据\n')


analysis = IthomeAnalysis()
analysis.main()
exit()
