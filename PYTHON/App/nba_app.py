# import time
# import pandas as pd
# import matplotlib.pyplot as plt
# import google.generativeai as genai
# import streamlit as st

# genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# df = pd.read_csv("player_stats.csv")

# st.set_page_config(page_title="NBA Ask-the-Data")
# st.title("NBA Ask-the-Data")


# user_query = st.text_input("Ask a question about the data:")

# if st.button("Run Query") and user_query:
#     code_prompt = f"""
# You are a Python pandas expert. Convert this question into valid pandas code using DataFrame `df`.
# The available columns are: {list(df.columns)}
# Query: \"{user_query}\"
# Return only the pandas code. Do not include markdown formatting (no ```python or ```).
# """
#     code_response = model.generate_content(code_prompt)
#     time.sleep(4)

   
#     lines = code_response.text.strip().splitlines()
#     code_lines = [line for line in lines if not line.strip().startswith("```")]
#     code = "\n".join(code_lines).strip()

#     if (
#         ".head" not in code
#         and ".tail" not in code
#         and ".plot" not in code
#         and "loc[" not in code
#         and "iloc[" not in code
#         and "[:10]" not in code
#     ):
#         code += ".head(10)" 

   
#     try:
#         result = eval(code)
#         explain_prompt = f"""
# The user asked: "{user_query}"

# Here’s the code that was run:
# {code}

# And the result was:
# {result.to_string() if isinstance(result, (pd.Series, pd.DataFrame)) else str(result)}

# Now explain the result in plain English like a chatbot would.
# """
#         explain_response = model.generate_content(explain_prompt)
#         time.sleep(4)

#         st.markdown("🤖 **Gemini's Explanation:**")
#         st.info(explain_response.text.strip())

#         st.success("✅ Query Result:")

#         plot_keywords = ["plot", "graph", "chart", "visual", "visualize", "bar", "line", "scatter"]
#         wants_plot = any(kw in user_query.lower() for kw in plot_keywords)

#         if wants_plot and hasattr(result, 'plot'):
#             fig = plt.figure(figsize=(8,4))
#             result.plot(kind='barh')  
#             st.pyplot(fig)  

#         elif isinstance(result, (str, int, float)):
#             st.write(result)

#         elif isinstance(result, (pd.Series, pd.DataFrame)):
#             st.dataframe(result)

#         else:
#             st.write(result)

#     except Exception as e:
#         st.error(f"Error running code:\n{e}")


import time
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

df = pd.read_csv("player_stats.csv")

st.set_page_config(page_title="NBA Ask-the-Data")
st.title("NBA Ask-the-Data")

user_query = st.text_input("Ask a question about the data:")

if st.button("Run Query") and user_query:
    code_prompt = f"""
You are a Python pandas expert. Convert this question into valid pandas code using DataFrame `df`.
The available columns are: {list(df.columns)}
Query: \"{user_query}\"
Return only the pandas code. Do not include markdown formatting (no ```python or ```).
"""
    code_response = model.generate_content(code_prompt)
    time.sleep(4)

    lines = code_response.text.strip().splitlines()
    code_lines = [line for line in lines if not line.strip().startswith("```")]
    code = "\n".join(code_lines).strip()

    if (
        ".head" not in code
        and ".tail" not in code
        and ".plot" not in code
        and "loc[" not in code
        and "iloc[" not in code
        and "[:10]" not in code
    ):
        code += ".head(10)" 

    try:
        result = eval(code)
        explain_prompt = f"""
The user asked: "{user_query}"

Here’s the code that was run:
{code}

And the result was:
{result.to_string() if isinstance(result, (pd.Series, pd.DataFrame)) else str(result)}

Now explain the result in plain English like a chatbot would.
"""
        explain_response = model.generate_content(explain_prompt)
        time.sleep(4)

        st.markdown("🤖 **Gemini's Explanation:**")
        st.info(explain_response.text.strip())

        st.success("Query Result:")

        if isinstance(result, (str, int, float)):
            st.write(result)

        elif isinstance(result, (pd.Series, pd.DataFrame)):
            st.dataframe(result)

        else:
            st.write(result)

    except Exception as e:
        st.error(f"Error running code:\n{e}")
