import random
import itertools
from typing import Any
from types import FunctionType
from types import MethodType
from abc import ABCMeta
from abc import abstractmethod

import pandas as pd
import numpy as np

class ConditionNode(object):
    TYPE_CRIT_RANDOM = 0
    TYPE_CRIT_BEST = 1
    
    IMP_FUNC_ENTROPY = 0
    IMP_FUNC_GINI = 1

    def __init__(self, condition: int           = None,
                       children: list           = [],
                       parent: Any              = None,
                       subset_indeces: set[int] = None,
                       value: int               = None):
        self.value: int                    = value
        self.condition: FunctionType       = condition
        self.children: list[ConditionNode] = children
        self.parent: ConditionNode         = parent
        self.subset_indeces: set[int]      = subset_indeces
        
    def _gini_impurity(self, y: pd.Series) -> float:
        if isinstance(y, pd.Series):
            prob: float = y.value_counts() / y.shape[0]
            gini: float = 1 - np.sum(prob ** 2)
            return gini
        else:
            raise Exception("y must be a pandas Series")
    
    def _scaled_entropy(self, y: pd.Series) -> float:
        if isinstance(y, pd.Series):
            prob: float    = y.value_counts() / y.shape[0]
            e: float       = 1e-9
            entropy: float = np.sum(-prob * np.log2(prob+e))
            return entropy
        else:
            raise Exception("y must be a pandas Series")

    def _information_gain(self, attr_series: pd.Series,
                                test_value: float,
                                is_categorical: bool,
                                imp_func: int = IMP_FUNC_ENTROPY) -> float:
        """
        imp_func: 0 = entropy, 1 = gini
        """
        imp_func: MethodType = self._scaled_entropy if imp_func == self.IMP_FUNC_ENTROPY else self._gini_impurity
        mask: pd.Series  = attr_series == test_value if is_categorical else attr_series <= test_value
        a: int   = sum(mask)
        b: int   = sum(~mask)
        tot: int = a + b
        return imp_func(self.df_y) - (a/tot)*imp_func(self.df_y[mask]) - (b/tot)*imp_func(self.df_y[~mask])
    
    def _generate_attribute_best(self, imp_func=IMP_FUNC_ENTROPY):
        # To choice the best feature to split
            # if the variable is in R:
                # threshold based splitting (quartile based splitting)          
            # else:imp_func
                # categorical based splitting (for each value of the feature)
            # choose the feature with the smallest/greatest ConditionNode.condition

        # y = self.df_y.take(list(self.root.subset_indeces))
        # gini = self.gini_impurity(y)
        # print("Gini: " + f"{gini:.5f}")
        return lambda x: 0 

    def _generate_attribute_random(self, imp_func: int = IMP_FUNC_ENTROPY) -> FunctionType:
        """
        imp_func: 0 = entropy, 1 = gini
        """
        index: int             = random.randint(0, len(self.df_x.columns) - 1)
        attr_name: str         = self.df_x.columns[index] # "Payment Currency"
        attr_series: pd.Series = self.df_x[attr_name]
        is_categorical = self.df_x.dtypes[index] == int and attr_series.nunique() < 20
        
        if is_categorical:
            possible_values: list[int] = attr_series.unique() 
        else:
            step = 0.20
            possible_values: list[float] = attr_series.quantile(np.arange(0, 1, step=step)).values
        
        print(f"Possible values: {possible_values}")

        best_val: float = -1.
        best_ig: float  = -1.
        for value in possible_values:
            information_gain: float = self._information_gain(attr_series, value, imp_func)
            if information_gain > best_ig:
                best_ig = information_gain
                best_val = value
        print(f"Best value: {best_val}")
        print(f"Best information gain: {best_ig}")
        
        if is_categorical:
            return lambda row: row[attr_name] == best_val
        else:
            return lambda row: row[attr_name] <= best_val
                    
    def generate_attribute(self, type_criterion: int = 0, imp_func: int = 0) -> FunctionType:
        """
        type_criterion: 0 = random, 1 = best
        imp_func: 0 = entropy, 1 = gini
        """
        if type_criterion == self.TYPE_CRIT_BEST:
            return self._generate_attribute_best(imp_func)
        else:
            return self._generate_attribute_random(imp_func)

    def get_labels(self) -> pd.Series:
        return self.df_y.take(list(self.subset_indeces))
    
    def set_df_x(self, df_x: pd.DataFrame):
        self.df_x = df_x
    
    def set_df_y(self, df_y: pd.DataFrame):
        self.df_y = df_y

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def str_dot(self) -> str:
        if self.is_leaf():
            return f"{self.value}"
        else:
            node_str: str = f"{self.value}"
            for i, child in enumerate(self.children):
                branch_str: str = f"{i}"
                child_str: str = child.str_dot().replace("\n", "\n\t")
                node_str += f"\n\t{branch_str} -> {child_str}"
            return node_str

class AbstractDecisionTree(object, metaclass=ABCMeta):
    def __init__(self, criterion, type_criterion, max_depth, min_samples_split):
        self.criterion = criterion
        self.type_criterion = type_criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        
    @abstractmethod
    def fit(self, df_x: pd.DataFrame, df_y: pd.DataFrame):
        self.root: ConditionNode = ConditionNode()
        self.root.value = round(sum(df_y) / len(df_y)) 
        self.root.subset_indeces = set(range(len(df_y)))   
        self.root.set_df_x(df_x)
        self.root.set_df_y(df_y)

    # TODO: add type hinting
    def __predict_rec(self, x, node: ConditionNode):
        val = None
        if node.is_leaf():
            val = node.value
        else:
            branch: int = node.condition(x)
            val = self.__predict_rec(x, node.children[branch])
        return val
   
    # TODO: add type hinting
    def predict(self, x): 
        self.__predict_rec(x, self.root)
        
    # TODO: add type hinting    
    def predict_train(self, x_list):
        for i in range(len(x_list)):
            yield self.predict(x_list[i])

    def str_dot(self) -> str:
        dot_str: str = "digraph DecisionTree {\n"
        dot_str += "\trankdir=TD;\n"
        dot_str += "\tnode [shape=box];\n"

        def traverse(node: ConditionNode, parent_id: str) -> str:
            node_id: str = str(id(node))
            dot_str: str = f"\t{node_id} [label=\"{node.str_dot()}\"];\n"
            if parent_id:
                dot_str += f"\t{parent_id} -> {node_id};\n"
            if not node.is_leaf():
                for child in node.children:
                    child_dot_str: str = traverse(child, node_id)
                    dot_str += child_dot_str
            return dot_str

        dot_str += traverse(self.root, "")
        dot_str += "}\n"
        return dot_str
    
    def create_dot_files(self, filename: str = "tree.dot", view: bool = False):
        with open(filename, "w") as f:
            f.write(self.str_dot())
        import subprocess
        command: str = f"dot -Tpng {filename} -o tree.png"
        subprocess.run(command, shell=True, check=True) 
        if view:
            command: str = "nohup xdg-open 'tree.png' >/dev/null 2>&1 &"
            subprocess.run(command, shell=True, check=True) 

    def __str__(self) -> str:
        return "AbstractDecisionTree"
