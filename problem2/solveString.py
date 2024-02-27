def replace_repeated_chars(s, k):
    result = []  # 保存结果

    for i, char in enumerate(s):

        """字符在它前面k个字符中已经出现过"""
        if char in s[max(0, i - k):i]:
            result.append('-')

        else:
            result.append(char)

    return ''.join(result)


if __name__ == '__main__':

    """获取输入，以空格分隔"""
    s, k = input().split()

    result = replace_repeated_chars(s, int(k))
    print(result)
