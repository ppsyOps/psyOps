*** Power SYstems OPerationS (psyops: si-ops) ***
***   is open source under the MIT License.   ***

GitHub: https://github.com/cadvena/psyOps

Installer is not yet built.  For now, copy the entire library to:
    C:\Python27\Lib\site-packages\psyops

Includes power systems Python scripts of three flavors:
    (1) Pure python extenstions (and a small cookbook)
	(2) Siemens PTI PSS/e extenstions 
	(3) PowerGEM TARA (AMD and PAAC) extensions
	
Goal Create a well-documented, easy to learn, power flow and analysis toolkit 
for professional power systems engineers. Not intended to replace tools like 
PSS/e, PowerWorld and TARA. Rather intended to validate the results of those 
projects, create a toolbox to leverage those systems and make your job as a 
power systems engineer easier.

Objectives 
1. Provide a well-documented, open source power flow analysis toolset. 
2. Wrap and extend psspy, the PSS/e Python library. 
3. Create a hacky PowerGEM TARA (AMB and PAAC) interface. 
4. Evolve into a gold standard power flow analysis toolset built and maintained 
   by engineers for the good of engineers.

Target Deliverables 
1. Fast, Newton-Raphson power flow engine. Solve very large power systems 
   models quickly. 
2. CIM and PSS/e compatibility: read CIM, raw, save, idev, inch and other files 
   standard to the grid operators in North America. 
3. Basic model management. Not a full-fledged model builder, just the basics 
   needed to make the tools useful. 
4. Extend psspy. Psspy is a python library for PSS/e that is provided by 
   Siemens PTI with their PSS/e product. This project will not modify psspy, 
   but will create extension libraries that depend on psspy for interactions 
   with PSS/e.
5. Write CIM compliant models and output.

Stretch Deliverables 
1. PSS/e <-> CIM model conversion. 
2. Advanced tools for security analysis, economic dispatch and more. 
3. Advanced model management tools like 2 <-> 3 winding conversion. 
4. Mapper tool to identify model changes and attempt to reconcile those 
   changes. Potential methods include node/equipment hybrid mapping. Node to 
   mode mapping. Auto identify which nodes can be identified as common. 
   Equipment mapping. Identify which equipment can be identified as common. 
   Provide three user mapping tools: node-to-node, equipment-to-equipment and 
   node/equipment.

