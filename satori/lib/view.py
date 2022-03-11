import pandas as pd
from matplotlib import pyplot as plt
from IPython.display import clear_output

class View:
    '''
    holds functionality for viewing model results
    '''

    def __init__(self):
        pass

    def pretty(x:dict):
        return ' ' + '\n '.join([f' {k}: {v}' for k, v in x.items()])

    def view(self, *args, **kwargs):
        self.print(*args, **kwargs)

    def print(self, *args, **kwargs):
        for arg in args:
            print(View.pretty(arg) if isinstance(arg, dict) else arg)
        for key, value in kwargs.items():
            print(key)
            print(View.pretty(value) if isinstance(value, dict) else value)


class JupyterView(View):
    '''
    holds functionality for viewing model results in a jupyter notebook
    '''

    def __init__(self, points:int=7):
        self.points = points

    def view(self, model, predictions:dict, scores:dict):
        self.jupyterOut(model, predictions, scores)

    def jupyterOut(self, model, predictions:dict, scores:dict):

        def lineWidth(score:str) -> float:
            try:
                score = (float(score.split()[0])+1)**3
            except:
                score = None
            return min(abs(score or .1), 1)

        #(model.data.iloc[-1*self.points:]
        #    .append(pd.DataFrame({k: [v] for k, v in predictions.items()}))
        #    .reset_index(drop=True)
        #    .plot(figsize=(8,5), linewidth=3))
        ## to show confidence with linewidth:
        ax = None
        for ix, col in enumerate(model.data.columns.tolist()):
            print(model.targetKey, predictions.get(col))
            ax = (model.data.iloc[-1*self.points:, [ix]]
                .append(pd.DataFrame({col: [predictions.get(col, 0)]}))
                .reset_index(drop=True)
                .plot(
                    **{'ax': ax} if ax is not None else {},
                    figsize=(8,5),
                    linewidth=lineWidth(scores.get(col, 0))))
        clear_output()
        plt.show()

# possible improvements:
# 1. optionally show graph of data with latest predictions
# 2. save all (best per datapoint, or per some amount of data or time)
#    models and predict every datapoint after them,
#    that way what they predict can be used as additional features.
#    this seems like a major feature that would require some archetecting.
#    maybe it can learn to keep the best 3 or something.
#    well, and then there's cyclical... idk
