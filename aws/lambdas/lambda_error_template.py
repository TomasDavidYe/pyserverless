LAMBDA_ERROR_TEMPLATE = '''
<p> Hello! </p>

<p>
    I am very sorry to tell you but a Lambda Function <span style="font-weight:bold">$(function_name) </span> from your <a href="https://trello.com/b/dXSzSqAs/trading-engine-with-kirill" target="_blank">Trading Engine </a>  project has crashed.
</p>

<p>
    Please go check it out in the <a href="https://eu-west-1.console.aws.amazon.com/console/home?nc2=h_ct&src=header-signin&region=eu-west-1" target="_blank">AWS Console </a>.
</p>

<p>
    You can find the details below:
</p>

<h3>Exception</h3>
<p>
$(exception)
</p>

<h3>Stack Trace</h3>
<p>
$(stack_trace)
</p>

<h3>Logs</h3>
<p>
$(log)
</p>

<h3>Full Response</h3>
<p>
    $(response)
</p>


<p>
Good Luck Fixing it !
</p>

<p>
Sincerely
</p>

<p>
Trading Engine :)
</p
'''
