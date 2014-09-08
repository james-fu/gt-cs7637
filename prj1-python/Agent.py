# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

from pprint import pprint


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a String representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These Strings
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName().
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(String givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will#not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # @param problem the RavensProblem your agent should solve
    # @return your Agent's answer to this problem
    def Solve(self, problem):
        oproblem = problem
        problem = self.pythonize(problem)
        pprint(problem)
        ret = '6'
        
        if problem['type'] == '2x1':
            target_trans = self.build_transform(problem['figures']['A'],
                                                problem['figures']['B'])
            pprint(target_trans)
            
            choice_trans = {}
            diffs = {}
            for i in range(1, 7):
                i = str(i)
                choice_trans[i] = self.build_transform(problem['figures']['C'],
                                                    problem['figures'][i])
                diffs[i] = self.compare_transforms(target_trans, choice_trans[i])
            
            pprint(diffs)
            
            ranked = sorted(diffs, key=diffs.get)
            # pick the one with the lowest diffs
            ret = ranked[0] 
            
            actual_answer = oproblem.checkAnswer(ret)
            if actual_answer == ret:
                print('CORRECT: chose %s' % ret)
            else:
                print('INCORRECT: chose %s, wanted %s' % (ret, actual_answer))
            
        x = raw_input('Press enter to continue, q to quit... ')
        if x.lower() == 'q':
            exit()
        return ret
    
    def compare_transforms(self, t1, t2):
        diffs = 0
        for t in t1:
            if not t in t2:
                diffs += 1
                continue
            if t1[t] != t2[t]:
                diffs += 1
        return diffs
    
    def build_transform(self, f1, f2):
        """Builds a transformation graph between two figures"""
        
        # TODO: handle different naming of shapes
        
        graph = {}
        
        for shape in f1:
            graph[shape] = []
            if not shape in f2:
                graph[shape] += ['deleted']
                continue
                
            if f2[shape].get('size', 0) > f1[shape].get('size', 0):
                graph[shape] += ['expanded']
            if f2[shape].get('size', 0) < f1[shape].get('size', 0):
                graph[shape] += ['shrunk']
            if f2[shape].get('fill', False) == True and \
                    f1[shape].get('fill', False) == False:
                graph[shape] += ['filled']
            if f2[shape].get('fill', False) == False and \
                    f1[shape].get('fill', False) == True:
                graph[shape] += ['unfilled']
            if f2[shape].get('shape', 'square') != f1[shape].get('shape', 'square'):
                graph[shape] += ['reshaped']
                
        
        return graph
    
    def parse_attr(self, name, value):
        lists = ['above', 'left-of', 'inside', 'overlaps']
        bools = ['fill', 'vertical-flip']#, 'horizontal-flip']
        sizes = ['size']
        nums = ['angle']
        shapes = ['shape']
        
        if name in lists:
            value = value.split(',')
        elif name in bools:
            if value == 'yes':
                value = True
            else:
                value = False
        elif name in sizes:
            if value == 'small':
                value = 1
            elif value == 'medium':
                value = 2
            elif value == 'large':
                value = 3
            else:
                value = 0
        elif name in nums:
            value = float(value)
        elif name in shapes:
            pass
        else:
            print "unknown: %s-%s" % (name, value)
        return value
        
    def pythonize(self, problem):
        """Returns a pythonic version of a problem object"""
        ret = {}
        
        figures = {}
        for fig in problem.getFigures().values():
            objs = {}
            for obj in fig.getObjects():
                attrs = {}
                for attr in obj.getAttributes():
                    attrs[attr.getName()] = self.parse_attr(attr.getName(), attr.getValue())
                objs[obj.getName()] = attrs
            figures[fig.getName()] = objs
            
        ret['type'] = problem.getProblemType()
        ret['name'] = problem.getName()
        ret['figures'] = figures
        return ret