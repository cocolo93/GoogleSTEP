#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

# 文字を読み取る
# 入力された文字が一致していれば token に追加
def read_function(line, index):
    character = ""
    while index < len(line) and line[index].isalpha():
        character += line[index]
        index += 1
    if character == "abs":
        token = {'type': 'ABS'}
    elif character == "round":
        token = {'type': 'ROUND'}
    elif character == "int":
        token = {'type': 'INT'}
    else:
        print('Invalid character found: ' + character)
        exit(1)
    return token, index

def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_times(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def read_start(line, index):
    token = {'type': 'START'}
    return token, index + 1

def read_end(line, index):
    token = {'type': 'END'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index].isalpha():
            (token, index) = read_function(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_times(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_start(line, index)
        elif line[index] == ')':
            (token, index) = read_end(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

# ()内の計算に対応
# (3*(4+5))のように括弧が複数になる場合も考えて再帰処理を行う。
def evaluate_brackets(tokens, start_index):
    index = start_index         # 再帰のたび変わるので変数に入れる
    new_tokens = []

    while index < len(tokens):
        if tokens[index]['type'] == 'START':
            calculate_ahead, new_index = evaluate_brackets(tokens, index + 1) # () がなくなるまでこの関数が呼び出され,
            calculate_ahead_answer = evaluate(calculate_ahead)                # evalate関数により()内の計算が行われる
            new_tokens.append({'type': 'NUMBER', 'number': calculate_ahead_answer})
            index = new_index
        elif tokens[index]['type'] == 'END':
            return new_tokens, index + 1
        else:
            new_tokens.append(tokens[index])
            index += 1

    return new_tokens, index

# abs, int, round に対応
def evaluate_abs_and_int_and_round(tokens):
    index = 0
    tokens, _ = evaluate_brackets(tokens, index)      # （） をなくした式にする。 ここでは戻り値のindexはいらないので省略
    new_tokens = []

    while index < len(tokens):
        # 負の数なら反転させる、正の数ならそのまま
        if tokens[index]['type'] == 'ABS':
            index += 1
            if tokens[index]['type'] == 'NUMBER':
                if tokens[index]['number'] >= 0:
                    calculate_answer = tokens[index]['number']
                else:
                    calculate_answer = - (tokens[index]['number'])
                new_tokens.append({'type': 'NUMBER', 'number': calculate_answer})

        # 符号が正の時 → caluculate_answerが NUMBER以下の間 1ずつ足していく。ループを抜けた後 -1 する。
        # 符号が負の時 → caluculate_answerが NUMBER以上の間 1ずつ引いていく。ループを抜けた後 +1 する。
        elif tokens[index]['type'] == 'INT':
            index += 1
            if tokens[index]['type'] == 'NUMBER':
                if tokens[index]['number'] >= 0:
                    calculate_answer = 0
                    while calculate_answer <= tokens[index]['number']:
                        calculate_answer += 1
                    calculate_answer -= 1
                else:
                    calculate_answer = 0
                    while calculate_answer >= tokens[index]['number']:
                        calculate_answer -= 1
                    calculate_answer += 1
                new_tokens.append({'type': 'NUMBER', 'number': calculate_answer})

        # 符号が正の時 → caluculate_answerが NUMBER以下の間 1ずつ 足していく。
        # ループ後の calculate_answer と元の NUMBERの差が 0.5より大きい場合(つまり少数が0.4以下の場合)
        # calculate_answerを　-1　する
        # 符号が負の時 → caluculate_answerがNUMBER以上の間 1ずつ 引いていく。
        # ループ後の calculate_answer と元の NUMBERの差が -0.5より小さい場合(つまり少数が0.4以下の場合)
        # calculate_answerを　+1　する
        elif tokens[index]['type'] == 'ROUND':
            index += 1
            if tokens[index]['type'] == 'NUMBER':
                if tokens[index]['number'] >= 0:
                    calculate_answer = 0
                    while calculate_answer <= tokens[index]['number']:
                        calculate_answer += 1
                    if calculate_answer - tokens[index]['number'] > 0.5:
                        calculate_answer -= 1
                else:
                    calculate_answer = 0
                    while calculate_answer >= tokens[index]['number']:
                        calculate_answer -= 1
                    if calculate_answer - tokens[index]['number'] < -0.5:
                        calculate_answer += 1
                new_tokens.append({'type': 'NUMBER', 'number': calculate_answer})
        else:
            new_tokens.append(tokens[index])
        index += 1

    return new_tokens

# *, / に対応
# tokenが NUMBER, PLUS(+), MINUS(-) であれば new_token に追加する
# TIMES(*), DIVIDE(/) であれば new_token に入っている最新の数字を取り出す。
# 取り出した数字(prev_number)と token の数字を計算し、結果を new_token に追加する
def evaluate_times_and_divide(tokens):
    index = 0
    tokens = evaluate_abs_and_int_and_round(tokens)
    new_tokens = []

    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            new_tokens.append(tokens[index])
        elif tokens[index]['type'] == 'TIMES':
            prev_number = new_tokens.pop()['number']
            index += 1
            if tokens[index]['type'] == 'NUMBER':
                prev_number *= tokens[index]['number']
                new_tokens.append({'type': 'NUMBER', 'number': prev_number})
        elif tokens[index]['type'] == 'DIVIDE':
            prev_number = new_tokens.pop()['number']
            index += 1
            if tokens[index]['type'] == 'NUMBER':
                prev_number /= tokens[index]['number']
                new_tokens.append({'type': 'NUMBER', 'number': prev_number})
        else:
            new_tokens.append(tokens[index])
        index += 1
    return new_tokens

def evaluate(tokens):
    answer = 0
    tokens = evaluate_times_and_divide(tokens) # *, / を評価した後のtokensにする
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
  
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test('3')
    test("1+2")
    test("1.5+4")
    test("4-1.5")
    test("1.0+2.1-3")
    test("5*2")
    test("8/2")
    test("2.5*1.0")
    test("3.9/1.3")
    test("2+3*3")
    test("4.3+2*8")
    test("10-8/2")
    test("10/2*3")
    test("10-(2-3)")
    test("1*(2-3)")
    test("(1.5+2)*(2+5.5)")
    test("30/15/3")
    test("30/(15/3)")
    test("120/(6*(5-3))")
    test("2.0*(4+2*(8/(4.5-2.5)))")
    test("abs(2.68)")
    test("abs(-2.68)")
    test("int(2.68)")
    test("int(-3.4)")
    test("round(2.2)")
    test("round(2.68)")
    test("round(-5.28)")
    test("round(-3.8)")
    test("10+abs(int(3.91-9.7)*round(5.7-2))")
    test("10*abs(int(3.91-9.7)*round(5.7-2)/(3+7))")
    # test("")
    # test("")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
