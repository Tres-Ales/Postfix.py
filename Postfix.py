import re

class Postfix:

    def __init__(self, infix_expression):
        self.__top = -1
        self.__stack = []
        self.__priority = {'+': 1, 
                          '-': 1,
                          '*': 2, 
                          '/': 2}
        self.__expression = []
        self.__val_expression = ""
        self.__result = None
        self.__to_postfix(infix_expression)
        
        self.variables = []
    #------------------------------------------------------------
        
    def __is_empty(self):
        return True if self.__top == -1 else False

    def __peek(self):
        return self.__stack[-1]

    def __push(self, el):
        self.__top += 1
        self.__stack.append(el)

    def __pop(self):
        if not self.__is_empty():
            self.__top -= 1
            return self.__stack.pop()
        return None
    
    def __is_var(self, el):
        return (el not in self.__priority.keys()) and (el not in "()")
    #el.isalpha()

    def __is_lower(self, op):
        try:
            left = self.__priority[op]
            top_el = self.__peek()
            right = self.__priority[top_el]
            return True if left <= right else False
        except:
            return False

    def __get_brackets(self):
        while (not self.__is_empty()) and (self.__peek() != '('):
            top_el = self.__pop()
            self.__expression += top_el

        if self.__is_empty(): 
            raise SyntaxError
        else: 
            self.__pop()
                
    def __unpack_stack(self, op):
        while (not self.__is_empty()) and self.__is_lower(op):
            top_el = self.__pop()
            self.__expression += top_el
        self.__push(op)
        
    def __parse(self, infix_expression):
        ops = "+-*/()"
        for op in ops:
            infix_expression = infix_expression.replace(op, ' ' + op + ' ')
        return infix_expression

    def __syntax_check(self, i, el, infix_expression):
        if (re.match('[a-z0-9*/+-]', el) == None) and (el not in "()") or (len(el) > 1):
            try:
                temp = float(el)
            except:
                return False
            #return False
        if el in self.__priority.keys():
            if i > 0 and i < len(infix_expression) and ((infix_expression[i-1] in self.__priority.keys()) or (infix_expression[i-1] in self.__priority.keys())):
                return False
        return True
                
    def __to_postfix(self, infix_expression):
        infix_expression = self.__parse(infix_expression).split()
        print('inf',infix_expression)
        for i, el in enumerate(infix_expression):
            if infix_expression[-1] in self.__priority.keys():
                raise SyntaxError
            if self.__syntax_check(i, el, infix_expression) != True:
                print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
                if el.isalpha() and re.match('[a-z]', el) == None:
                    raise NameError
                raise SyntaxError
            #print('el', el)
            if el == '-' and (i == 0 or infix_expression[i-1] == '('):
                continue
                
            if self.__is_var(el):
                
                if i != 0:
                    if infix_expression[i-1] == '-' and infix_expression[i-2] == '(':
                         self.__expression.append(el)
                         self.__expression.append('!')
                    elif infix_expression[i-1] == '-' and i == 1:
                         self.__expression.append(el)
                         self.__expression.append('!')
                    else:
                         self.__expression.append(el)
                else:
                    self.__expression.append(el)
                
            elif el == '(':
                self.__push(el)

            elif el == ')':
                self.__get_brackets()

            else:
                self.__unpack_stack(el)
            #print(self.__stack)
            #print(self.__expression)
            
        while not self.__is_empty():
            top_el = self.__pop()
            if top_el == '(':
                raise SyntaxError
            self.__expression.append(top_el)
        #print(self.__expression)

    def __extract_variables(self):
        #print(self.__expression)
        #print(re.sub('[^a-z0-9]', ' ', str(self.__expression)).split())
        variables = re.sub('[^a-z]', ' ', str(self.__expression)).split()
        #if len(variables) == 0 and len(re.sub('[^a-z0-9]', ' ', str(self.__expression))) == 0:
        #    raise NameError
        unique_vars = []
        for var in variables:
            if var not in unique_vars:
                unique_vars.append(var)
        return unique_vars
    
    def __input(self):
        
        variables = self.__extract_variables()
        #print(variables)
        var_values = {}
        self.variables = [None]*len(variables)
        for i, var in enumerate(variables):
            value = input(f"Введите значение {var}: ")
            var_values[var] = value
            self.variables[i] = float(value)
        return var_values

    def __replace_with_values(self):
        
        var_values = self.__input()
        self.__val_expression = ' '.join(self.__expression)
        #print('exp', self.__expression)
        for var in var_values.keys():
            self.__val_expression = self.__val_expression.replace(var, var_values.get(var))
        #print('val', self.__val_expression)

    def __switch(self, left, right, op):
        if op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                raise ZeroDivisionError
            else:
                return left / right
        elif op == '+':
            return left + right
        else:
            return left - right
    #------------------------------------------------------------

    def get_expression(self):
        return ' '.join(self.__expression)
    
    def get_val_expression(self):
        return ''.join(self.__val_expression).replace(' ', '')

    def evaluate(self):
        self.__replace_with_values()
        list_expression = self.__val_expression.split(' ')
        #print(list_expression)
        self.__stack = []
        #print(self.__stack)
        for i, el in enumerate(list_expression):
            #print(el)
            if el == '!':
                continue
            
            if el in self.__priority.keys():
                right = self.__pop()
                left = self.__pop()
                #print(f"{left} {el} {right}")
                try:
                    temp = self.__switch(left, right, el)
                    #print('temp' , temp)
                    self.__push(temp)
                    #print('peek ', self.__peek())
                except ZeroDivisionError:
                    raise
            else:
                #print('412')
                #if '.' in el:
                if i != len(list_expression) - 1 and list_expression[i+1] == '!':
                    self.__push((-1)*float(el))
                else:
                    self.__push(float(el))
                    #print('afa')
                #else:
                #    if list_expression[i+1] == '!':
                #        self.__push((-1)*int(el))
                #    else:
                #        self.__push(int(el))
            #print(self.__stack)
        self.__result = self.__pop()  
        return self.__result   
            
    def get_result(self):
        return self.__result





    
