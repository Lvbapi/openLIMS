import re
# import numpy

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = codecs.encode(word, 'translit/long')
        if word:
            result.append(word)
    return str(delim.join(result))


# def get_z_score_outliers(data_set):
#     outliers = []
#     threshold = 3
#     mean = numpy.mean(data_set)
#     standard_deviation =numpy.std(data_set)
    
#     for data_point in data_set:
#         z_score = (data_point - mean) / standard_deviation 
#         if numpy.abs(z_score) > threshold:
#             outliers.append(data_point)
#     return outliers


# def get_iqr_range(data_set):
#     sorted(data_set)
#     q1, q3 = numpy.percentile(data_set,[25,75])
#     iqr = q3 - q1
#     lower_bound = q1 - (1.5 * iqr) 
#     upper_bound = q3 + (1.5 * iqr)

#     return {'lower_bound': lower_bound, 'upper_bound': upper_bound}
