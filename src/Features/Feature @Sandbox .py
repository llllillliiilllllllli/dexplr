from Functions.DataAnalysis import Analyzer

class Sandbox:

    def demo_analyzer():
        import pandas as pd
        data = {
            "Words": ["Tom", "Helen", "Nick", "Juli"],
            "Sents": [
                "Tom is a student at school.", 
                "Helen is a staff at office.", 
                "Nick is a farmer on the field.", 
                "Juli is an investor on the market."],
            "Paras": [
                "Tom is a student at school. Helen is a staff at office.", 
                "Helen is a staff at office. Nick is a farmer on the field.", 
                "Nick is a farmer on the field. Juli is an investor on the market.", 
                "Juli is an investor on the market. Tom is a student at school."]
        }

        df = pd.DataFrame(data, dtype="string")
        
        Analyzer.desribe_text(df["Words"])
        Analyzer.desribe_text(df["Sents"])
        Analyzer.desribe_text(df["Paras"])
