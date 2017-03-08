[1mdiff --git a/Face spoof detection/Implementation/.idea/workspace.xml b/Face spoof detection/Implementation/.idea/workspace.xml[m
[1mindex df81ff4..dd868e3 100644[m
[1m--- a/Face spoof detection/Implementation/.idea/workspace.xml[m	
[1m+++ b/Face spoof detection/Implementation/.idea/workspace.xml[m	
[36m@@ -2,13 +2,11 @@[m
 <project version="4">[m
   <component name="ChangeListManager">[m
     <list default="true" id="61659cf9-0a32-498f-b4cd-80bbe55b95db" name="Default" comment="">[m
[31m-      <change type="DELETED" beforePath="$PROJECT_DIR$/testingFeatures.py" afterPath="" />[m
[31m-      <change type="MODIFICATION" beforePath="$PROJECT_DIR$/../../.gitignore" afterPath="$PROJECT_DIR$/../../.gitignore" />[m
       <change type="MODIFICATION" beforePath="$PROJECT_DIR$/.idea/workspace.xml" afterPath="$PROJECT_DIR$/.idea/workspace.xml" />[m
       <change type="MODIFICATION" beforePath="$PROJECT_DIR$/alignDlibDemo.py" afterPath="$PROJECT_DIR$/alignDlibDemo.py" />[m
[32m+[m[32m      <change type="MODIFICATION" beforePath="$PROJECT_DIR$/faceSpoofValidation.py" afterPath="$PROJECT_DIR$/faceSpoofValidation.py" />[m
       <change type="MODIFICATION" beforePath="$PROJECT_DIR$/features.py" afterPath="$PROJECT_DIR$/features.py" />[m
       <change type="MODIFICATION" beforePath="$PROJECT_DIR$/main.py" afterPath="$PROJECT_DIR$/main.py" />[m
[31m-      <change type="MODIFICATION" beforePath="$PROJECT_DIR$/../../FaceSpoofingNotes.txt" afterPath="$PROJECT_DIR$/../../FaceSpoofingNotes.txt" />[m
     </list>[m
     <option name="EXCLUDED_CONVERTED_TO_IGNORED" value="true" />[m
     <option name="TRACKING_ENABLED" value="true" />[m
[36m@@ -18,11 +16,11 @@[m
     <option name="LAST_RESOLUTION" value="IGNORE" />[m
   </component>[m
   <component name="CoverageDataManager">[m
[31m-    <SUITE FILE_PATH="coverage/Implementation$main.coverage" NAME="main Coverage Results" MODIFIED="1487949864533" SOURCE_PROVIDER="com.intellij.coverage.DefaultCoverageFileProvider" RUNNER="coverage.py" COVERAGE_BY_TEST_ENABLED="true" COVERAGE_TRACING_ENABLED="false" WORKING_DIRECTORY="$PROJECT_DIR$" />[m
[32m+[m[32m    <SUITE FILE_PATH="coverage/Implementation$main.coverage" NAME="main Coverage Results" MODIFIED="1488879168998" SOURCE_PROVIDER="com.intellij.coverage.DefaultCoverageFileProvider" RUNNER="coverage.py" COVERAGE_BY_TEST_ENABLED="true" COVERAGE_TRACING_ENABLED="false" WORKING_DIRECTORY="$PROJECT_DIR$" />[m
     <SUITE FILE_PATH="coverage/Implementation$vlfeatTest.coverage" NAME="vlfeatTest Coverage Results" MODIFIED="1488830115693" SOURCE_PROVIDER="com.intellij.coverage.DefaultCoverageFileProvider" RUNNER="coverage.py" COVERAGE_BY_TEST_ENABLED="true" COVERAGE_TRACING_ENABLED="false" WORKING_DIRECTORY="$PROJECT_DIR$" />[m
     <SUITE FILE_PATH="coverage/Implementation$featureSpeedTesting.coverage" NAME="featureSpeedTesting Coverage Results" MODIFIED="1488831372210" SOURCE_PROVIDER="com.intellij.coverage.DefaultCoverageFileProvider" RUNNER="coverage.py" COVERAGE_BY_TEST_ENABLED="true" COVERAGE_TRACING_ENABLED="false" WORKING_DIRECTORY="$PROJECT_DIR$" />[m
     <SUITE FILE_PATH="coverage/Implementation$testingFeatures.coverage" NAME="testingFeatures Coverage Results" MODIFIED="1488823835491" SOURCE_PROVIDER="com.intellij.coverage.DefaultCoverageFileProvider" RUNNER="coverage.py" COVERAGE_BY_TEST_ENABLED="true" COVERAGE_TRACING_ENABLED="false" WORKING_DIRECTORY="$PROJECT_DIR$" />[m
[31m-    <SUITE FILE_PATH="coverage/Implementation$alignDlibDemo.coverage" NAME="alignDlibDemo Coverage Results" MODIFIED="1488824337614" SOURCE_PROVIDER="com.intellij.coverage.DefaultCoverageFileProvider" RUNNER="coverage.py" COVERAGE_BY_TEST_ENABLED="true" COVERAGE_TRACING_ENABLED="false" WORKING_DIRECTORY="$PROJECT_DIR$" />[m
[32m+[m[32m    <SUITE FILE_PATH="coverage/Implementation$alignDlibDemo.coverage" NAME="alignDlibDemo Coverage Results" MODIFIED="1488877198625" SOURCE_PROVIDER="com.intellij.coverage.DefaultCoverageFileProvider" RUNNER="coverage.py" COVERAGE_BY_TEST_ENABLED="true" COVERAGE_TRACING_ENABLED="false" WORKING_DIRECTORY="$PROJECT_DIR$" />[m
   </component>[m
   <component name="CreatePatchCommitExecutor">[m
     <option name="PATCH_PATH" value="" />[m
[36m@@ -44,20 +42,44 @@[m
       <file leaf-file-name="features.py" pinned="false" current-in-tab="false">[m
         <entry file="file://$PROJECT_DIR$/features.py">[m
           <provider selected="true" editor-type-id="text-editor">[m
[31m-            <state relative-caret-position="551">[m
[31m-              <caret line="75" column="22" lean-forward="false" selection-start-line="75" selection-start-column="22" selection-end-line="75" selection-end-column="22" />[m
[32m+[m[32m            <state relative-caret-position="467">[m
[32m+[m[32m              <caret line="76" column="0" lean-forward="false" selection-start-line="76" selection-start-column="0" selection-end-line="76" selection-end-column="0" />[m
               <folding>[m
[31m-                <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m                <element signature="e#0#18#0" expanded="true" />[m
[32m+[m[32m              </folding>[m
[32m+[m[32m            </state>[m
[32m+[m[32m          </provider>[m
[32m+[m[32m        </entry>[m
[32m+[m[32m      </file>[m
[32m+[m[32m      <file leaf-file-name="main.py" pinned="false" current-in-tab="false">[m
[32m+[m[32m        <entry file="file://$PROJECT_DIR$/main.py">[m
[32m+[m[32m          <provider selected="true" editor-type-id="text-editor">[m
[32m+[m[32m            <state relative-caret-position="1911">[m
[32m+[m[32m              <caret line="139" column="52" lean-forward="false" selection-start-line="139" selection-start-column="52" selection-end-line="139" selection-end-column="52" />[m
[32m+[m[32m              <folding>[m
[32m+[m[32m                <element signature="e#427#1455#0" expanded="false" />[m
               </folding>[m
             </state>[m
           </provider>[m
         </entry>[m
       </file>[m
[31m-      <file leaf-file-name="alignDlibDemo.py" pinned="false" current-in-tab="true">[m
[32m+[m[32m      <file leaf-file-name="faceSpoofValidation.py" pinned="false" current-in-tab="true">[m
[32m+[m[32m        <entry file="file://$PROJECT_DIR$/faceSpoofValidation.py">[m
[32m+[m[32m          <provider selected="true" editor-type-id="text-editor">[m
[32m+[m[32m            <state relative-caret-position="441">[m
[32m+[m[32m              <caret line="21" column="31" lean-forward="false" selection-start-line="21" selection-start-column="31" selection-end-line="21" selection-end-column="31" />[m
[32m+[m[32m              <folding>[m
[32m+[m[32m                <element signature="e#0#10#0" expanded="true" />[m
[32m+[m[32m              </folding>[m
[32m+[m[32m            </state>[m
[32m+[m[32m          </provider>[m
[32m+[m[32m        </entry>[m
[32m+[m[32m      </file>[m
[32m+[m[32m      <file leaf-file-name="alignDlibDemo.py" pinned="false" current-in-tab="false">[m
         <entry file="file://$PROJECT_DIR$/alignDlibDemo.py">[m
           <provider selected="true" editor-type-id="text-editor">[m
[31m-            <state relative-caret-position="147">[m
[31m-              <caret line="70" column="0" lean-forward="false" selection-start-line="70" selection-start-column="0" selection-end-line="70" selection-end-column="0" />[m
[32m+[m[32m            <state relative-caret-position="71">[m
[32m+[m[32m              <caret line="52" column="8" lean-forward="false" selection-start-line="52" selection-start-column="8" selection-end-line="52" selection-end-column="8" />[m
               <folding>[m
                 <element signature="e#0#10#0" expanded="true" />[m
               </folding>[m
[36m@@ -65,6 +87,16 @@[m
           </provider>[m
         </entry>[m
       </file>[m
[32m+[m[32m      <file leaf-file-name="testingLBP.py" pinned="false" current-in-tab="false">[m
[32m+[m[32m        <entry file="file://$PROJECT_DIR$/testingLBP.py">[m
[32m+[m[32m          <provider selected="true" editor-type-id="text-editor">[m
[32m+[m[32m            <state relative-caret-position="-1696">[m
[32m+[m[32m              <caret line="15" column="41" lean-forward="false" selection-start-line="15" selection-start-column="41" selection-end-line="15" selection-end-column="41" />[m
[32m+[m[32m              <folding />[m
[32m+[m[32m            </state>[m
[32m+[m[32m          </provider>[m
[32m+[m[32m        </entry>[m
[32m+[m[32m      </file>[m
       <file leaf-file-name="vlfeatTest.py" pinned="false" current-in-tab="false">[m
         <entry file="file://$PROJECT_DIR$/vlfeatTest.py">[m
           <provider selected="true" editor-type-id="text-editor">[m
[36m@@ -80,7 +112,7 @@[m
       <file leaf-file-name="featureSpeedTesting.py" pinned="false" current-in-tab="false">[m
         <entry file="file://$PROJECT_DIR$/featureSpeedTesting.py">[m
           <provider selected="true" editor-type-id="text-editor">[m
[31m-            <state relative-caret-position="501">[m
[32m+[m[32m            <state relative-caret-position="1407">[m
               <caret line="73" column="29" lean-forward="false" selection-start-line="73" selection-start-column="29" selection-end-line="73" selection-end-column="29" />[m
               <folding>[m
                 <marker date="1488832020602" expanded="true" signature="623:1235" ph="'''...'''" />[m
[36m@@ -105,13 +137,13 @@[m
     <option name="CHANGED_PATHS">[m
       <list>[m
         <option value="$PROJECT_DIR$/specular_reflection.py" />[m
[31m-        <option value="$PROJECT_DIR$/faceSpoofValidation.py" />[m
[31m-        <option value="$PROJECT_DIR$/main.py" />[m
         <option value="$PROJECT_DIR$/testingFeatures.py" />[m
         <option value="$PROJECT_DIR$/vlfeatTest.py" />[m
[31m-        <option value="$PROJECT_DIR$/features.py" />[m
         <option value="$PROJECT_DIR$/featureSpeedTesting.py" />[m
         <option value="$PROJECT_DIR$/alignDlibDemo.py" />[m
[32m+[m[32m        <option value="$PROJECT_DIR$/main.py" />[m
[32m+[m[32m        <option value="$PROJECT_DIR$/faceSpoofValidation.py" />[m
[32m+[m[32m        <option value="$PROJECT_DIR$/features.py" />[m
       </list>[m
     </option>[m
   </component>[m
[36m@@ -143,7 +175,6 @@[m
       <foldersAlwaysOnTop value="true" />[m
     </navigator>[m
     <panes>[m
[31m-      <pane id="Scope" />[m
       <pane id="Scratches" />[m
       <pane id="ProjectPane">[m
         <subPane>[m
[36m@@ -159,6 +190,7 @@[m
           </PATH>[m
         </subPane>[m
       </pane>[m
[32m+[m[32m      <pane id="Scope" />[m
     </panes>[m
   </component>[m
   <component name="PropertiesComponent">[m
[36m@@ -167,7 +199,7 @@[m
     <property name="settings.editor.selected.configurable" value="preferences.pluginManager" />[m
     <property name="last_opened_file_path" value="$PROJECT_DIR$" />[m
   </component>[m
[31m-  <component name="RunManager" selected="Python.featureSpeedTesting">[m
[32m+[m[32m  <component name="RunManager" selected="Python.main">[m
     <configuration default="false" name="main" type="PythonConfigurationType" factoryName="Python" temporary="true">[m
       <option name="INTERPRETER_OPTIONS" value="" />[m
       <option name="PARENT_ENVS" value="true" />[m
[36m@@ -481,11 +513,11 @@[m
     </list>[m
     <recent_temporary>[m
       <list size="5">[m
[31m-        <item index="0" class="java.lang.String" itemvalue="Python.featureSpeedTesting" />[m
[31m-        <item index="1" class="java.lang.String" itemvalue="Python.vlfeatTest" />[m
[31m-        <item index="2" class="java.lang.String" itemvalue="Python.alignDlibDemo" />[m
[31m-        <item index="3" class="java.lang.String" itemvalue="Python.testingFeatures" />[m
[31m-        <item index="4" class="java.lang.String" itemvalue="Python.main" />[m
[32m+[m[32m        <item index="0" class="java.lang.String" itemvalue="Python.main" />[m
[32m+[m[32m        <item index="1" class="java.lang.String" itemvalue="Python.alignDlibDemo" />[m
[32m+[m[32m        <item index="2" class="java.lang.String" itemvalue="Python.featureSpeedTesting" />[m
[32m+[m[32m        <item index="3" class="java.lang.String" itemvalue="Python.vlfeatTest" />[m
[32m+[m[32m        <item index="4" class="java.lang.String" itemvalue="Python.testingFeatures" />[m
       </list>[m
     </recent_temporary>[m
   </component>[m
[36m@@ -515,11 +547,10 @@[m
     <frame x="61" y="24" width="1859" height="1056" extended-state="6" />[m
     <editor active="true" />[m
     <layout>[m
[31m-      <window_info id="Project" active="false" anchor="left" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="true" show_stripe_button="true" weight="0.23000552" sideWeight="0.4896" order="0" side_tool="false" content_ui="combo" />[m
[32m+[m[32m      <window_info id="Project" active="false" anchor="left" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="true" show_stripe_button="true" weight="0.23276338" sideWeight="0.4896" order="0" side_tool="false" content_ui="combo" />[m
       <window_info id="TODO" active="false" anchor="bottom" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="false" show_stripe_button="true" weight="0.32903227" sideWeight="0.5" order="6" side_tool="false" content_ui="tabs" />[m
       <window_info id="Event Log" active="false" anchor="bottom" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="false" show_stripe_button="true" weight="0.32903227" sideWeight="0.5" order="7" side_tool="true" content_ui="tabs" />[m
       <window_info id="Database" active="false" anchor="right" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="false" show_stripe_button="true" weight="0.33" sideWeight="0.5" order="3" side_tool="false" content_ui="tabs" />[m
[31m-      <window_info id="Find" active="false" anchor="bottom" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="false" show_stripe_button="true" weight="0.32903227" sideWeight="0.5" order="1" side_tool="false" content_ui="tabs" />[m
       <window_info id="Version Control" active="false" anchor="bottom" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="false" show_stripe_button="true" weight="0.32903227" sideWeight="0.5" order="7" side_tool="false" content_ui="tabs" />[m
       <window_info id="Python Console" active="false" anchor="bottom" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="false" show_stripe_button="true" weight="0.2360515" sideWeight="0.5" order="7" side_tool="false" content_ui="tabs" />[m
       <window_info id="Run" active="false" anchor="bottom" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="true" show_stripe_button="true" weight="0.3075269" sideWeight="0.5" order="2" side_tool="false" content_ui="tabs" />[m
[36m@@ -532,6 +563,7 @@[m
       <window_info id="Commander" active="false" anchor="right" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="false" show_stripe_button="true" weight="0.4" sideWeight="0.5" order="0" side_tool="false" content_ui="tabs" />[m
       <window_info id="Inspection" active="false" anchor="bottom" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="false" show_stripe_button="true" weight="0.4" sideWeight="0.5" order="5" side_tool="false" content_ui="tabs" />[m
       <window_info id="Hierarchy" active="false" anchor="right" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="false" show_stripe_button="true" weight="0.25" sideWeight="0.5" order="2" side_tool="false" content_ui="combo" />[m
[32m+[m[32m      <window_info id="Find" active="false" anchor="bottom" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="false" show_stripe_button="true" weight="0.32903227" sideWeight="0.5" order="1" side_tool="false" content_ui="tabs" />[m
       <window_info id="Ant Build" active="false" anchor="right" auto_hide="false" internal_type="DOCKED" type="DOCKED" visible="false" show_stripe_button="true" weight="0.25" sideWeight="0.5" order="1" side_tool="false" content_ui="tabs" />[m
     </layout>[m
     <layout-to-restore>[m
[36m@@ -570,11 +602,6 @@[m
           <option name="timeStamp" value="7" />[m
         </line-breakpoint>[m
         <line-breakpoint enabled="true" suspend="THREAD" type="python-line">[m
[31m-          <url>file://$PROJECT_DIR$/alignDlibDemo.py</url>[m
[31m-          <line>69</line>[m
[31m-          <option name="timeStamp" value="20" />[m
[31m-        </line-breakpoint>[m
[31m-        <line-breakpoint enabled="true" suspend="THREAD" type="python-line">[m
           <url>file://$PROJECT_DIR$/featureSpeedTesting.py</url>[m
           <line>75</line>[m
           <option name="timeStamp" value="21" />[m
[36m@@ -589,6 +616,11 @@[m
           <line>65</line>[m
           <option name="timeStamp" value="29" />[m
         </line-breakpoint>[m
[32m+[m[32m        <line-breakpoint enabled="true" suspend="THREAD" type="python-line">[m
[32m+[m[32m          <url>file://$PROJECT_DIR$/faceSpoofValidation.py</url>[m
[32m+[m[32m          <line>13</line>[m
[32m+[m[32m          <option name="timeStamp" value="33" />[m
[32m+[m[32m        </line-breakpoint>[m
       </breakpoints>[m
       <breakpoints-dialog>[m
         <breakpoints-dialog />[m
[36m@@ -600,7 +632,7 @@[m
           </properties>[m
         </breakpoint>[m
       </default-breakpoints>[m
[31m-      <option name="time" value="30" />[m
[32m+[m[32m      <option name="time" value="34" />[m
     </breakpoint-manager>[m
     <watches-manager />[m
   </component>[m
[36m@@ -634,7 +666,7 @@[m
         <state relative-caret-position="147">[m
           <caret line="8" column="27" lean-forward="false" selection-start-line="8" selection-start-column="27" selection-end-line="8" selection-end-column="27" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -643,9 +675,7 @@[m
       <provider selected="true" editor-type-id="text-editor">[m
         <state relative-caret-position="1575">[m
           <caret line="75" column="0" lean-forward="false" selection-start-line="75" selection-start-column="0" selection-end-line="75" selection-end-column="0" />[m
[31m-          <folding>[m
[31m-            <element signature="e#0#37#0" expanded="true" />[m
[31m-          </folding>[m
[32m+[m[32m          <folding />[m
         </state>[m
       </provider>[m
     </entry>[m
[36m@@ -678,7 +708,7 @@[m
         <state relative-caret-position="147">[m
           <caret line="8" column="27" lean-forward="false" selection-start-line="8" selection-start-column="27" selection-end-line="8" selection-end-column="27" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -687,9 +717,7 @@[m
       <provider selected="true" editor-type-id="text-editor">[m
         <state relative-caret-position="1575">[m
           <caret line="75" column="0" lean-forward="false" selection-start-line="75" selection-start-column="0" selection-end-line="75" selection-end-column="0" />[m
[31m-          <folding>[m
[31m-            <element signature="e#0#37#0" expanded="true" />[m
[31m-          </folding>[m
[32m+[m[32m          <folding />[m
         </state>[m
       </provider>[m
     </entry>[m
[36m@@ -722,7 +750,7 @@[m
         <state relative-caret-position="882">[m
           <caret line="43" column="50" lean-forward="false" selection-start-line="43" selection-start-column="50" selection-end-line="43" selection-end-column="50" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -731,9 +759,7 @@[m
       <provider selected="true" editor-type-id="text-editor">[m
         <state relative-caret-position="0">[m
           <caret line="0" column="0" lean-forward="false" selection-start-line="0" selection-start-column="0" selection-end-line="0" selection-end-column="0" />[m
[31m-          <folding>[m
[31m-            <element signature="e#0#37#0" expanded="true" />[m
[31m-          </folding>[m
[32m+[m[32m          <folding />[m
         </state>[m
       </provider>[m
     </entry>[m
[36m@@ -749,7 +775,7 @@[m
         <state relative-caret-position="0">[m
           <caret line="0" column="0" lean-forward="false" selection-start-line="0" selection-start-column="0" selection-end-line="0" selection-end-column="0" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -758,9 +784,7 @@[m
       <provider selected="true" editor-type-id="text-editor">[m
         <state relative-caret-position="1323">[m
           <caret line="63" column="0" lean-forward="false" selection-start-line="63" selection-start-column="0" selection-end-line="63" selection-end-column="0" />[m
[31m-          <folding>[m
[31m-            <element signature="e#0#37#0" expanded="true" />[m
[31m-          </folding>[m
[32m+[m[32m          <folding />[m
         </state>[m
       </provider>[m
     </entry>[m
[36m@@ -776,7 +800,7 @@[m
         <state relative-caret-position="0">[m
           <caret line="0" column="0" lean-forward="false" selection-start-line="0" selection-start-column="0" selection-end-line="0" selection-end-column="0" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -785,9 +809,7 @@[m
       <provider selected="true" editor-type-id="text-editor">[m
         <state relative-caret-position="1302">[m
           <caret line="62" column="54" lean-forward="false" selection-start-line="62" selection-start-column="54" selection-end-line="62" selection-end-column="54" />[m
[31m-          <folding>[m
[31m-            <element signature="e#0#37#0" expanded="true" />[m
[31m-          </folding>[m
[32m+[m[32m          <folding />[m
         </state>[m
       </provider>[m
     </entry>[m
[36m@@ -796,7 +818,7 @@[m
         <state relative-caret-position="336">[m
           <caret line="17" column="0" lean-forward="false" selection-start-line="17" selection-start-column="0" selection-end-line="17" selection-end-column="0" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -805,9 +827,7 @@[m
       <provider selected="true" editor-type-id="text-editor">[m
         <state relative-caret-position="1302">[m
           <caret line="62" column="54" lean-forward="false" selection-start-line="62" selection-start-column="54" selection-end-line="62" selection-end-column="54" />[m
[31m-          <folding>[m
[31m-            <element signature="e#0#37#0" expanded="true" />[m
[31m-          </folding>[m
[32m+[m[32m          <folding />[m
         </state>[m
       </provider>[m
     </entry>[m
[36m@@ -816,7 +836,7 @@[m
         <state relative-caret-position="0">[m
           <caret line="0" column="0" lean-forward="false" selection-start-line="0" selection-start-column="0" selection-end-line="0" selection-end-column="0" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -832,9 +852,7 @@[m
       <provider selected="true" editor-type-id="text-editor">[m
         <state relative-caret-position="1113">[m
           <caret line="53" column="0" lean-forward="false" selection-start-line="53" selection-start-column="0" selection-end-line="53" selection-end-column="0" />[m
[31m-          <folding>[m
[31m-            <element signature="e#0#37#0" expanded="true" />[m
[31m-          </folding>[m
[32m+[m[32m          <folding />[m
         </state>[m
       </provider>[m
     </entry>[m
[36m@@ -849,9 +867,7 @@[m
       <provider selected="true" editor-type-id="text-editor">[m
         <state relative-caret-position="1197">[m
           <caret line="57" column="0" lean-forward="false" selection-start-line="57" selection-start-column="0" selection-end-line="57" selection-end-column="0" />[m
[31m-          <folding>[m
[31m-            <element signature="e#0#37#0" expanded="true" />[m
[31m-          </folding>[m
[32m+[m[32m          <folding />[m
         </state>[m
       </provider>[m
     </entry>[m
[36m@@ -860,7 +876,7 @@[m
         <state relative-caret-position="357">[m
           <caret line="18" column="24" lean-forward="false" selection-start-line="18" selection-start-column="24" selection-end-line="18" selection-end-column="24" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -877,7 +893,7 @@[m
         <state relative-caret-position="273">[m
           <caret line="13" column="18" lean-forward="false" selection-start-line="13" selection-start-column="18" selection-end-line="13" selection-end-column="18" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -894,7 +910,7 @@[m
         <state relative-caret-position="378">[m
           <caret line="18" column="24" lean-forward="false" selection-start-line="18" selection-start-column="24" selection-end-line="18" selection-end-column="24" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -911,7 +927,7 @@[m
         <state relative-caret-position="357">[m
           <caret line="18" column="24" lean-forward="false" selection-start-line="18" selection-start-column="24" selection-end-line="18" selection-end-column="24" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -928,7 +944,7 @@[m
         <state relative-caret-position="378">[m
           <caret line="18" column="24" lean-forward="false" selection-start-line="18" selection-start-column="24" selection-end-line="18" selection-end-column="24" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -945,7 +961,7 @@[m
         <state relative-caret-position="0">[m
           <caret line="0" column="0" lean-forward="false" selection-start-line="0" selection-start-column="0" selection-end-line="0" selection-end-column="0" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
[36m@@ -967,66 +983,68 @@[m
         </state>[m
       </provider>[m
     </entry>[m
[31m-    <entry file="file://$PROJECT_DIR$/testingLBP.py">[m
[32m+[m[32m    <entry file="file://$PROJECT_DIR$/vlfeatTest.py">[m
       <provider selected="true" editor-type-id="text-editor">[m
[31m-        <state relative-caret-position="-381">[m
[31m-          <caret line="15" column="41" lean-forward="false" selection-start-line="15" selection-start-column="41" selection-end-line="15" selection-end-column="41" />[m
[32m+[m[32m        <state relative-caret-position="336">[m
[32m+[m[32m          <caret line="16" column="0" lean-forward="false" selection-start-line="16" selection-start-column="0" selection-end-line="16" selection-end-column="0" />[m
           <folding>[m
[31m-            <element signature="e#0#37#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#27#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
     </entry>[m
[31m-    <entry file="file://$PROJECT_DIR$/main.py">[m
[32m+[m[32m    <entry file="file://$PROJECT_DIR$/featureSpeedTesting.py">[m
       <provider selected="true" editor-type-id="text-editor">[m
[31m-        <state relative-caret-position="417">[m
[31m-          <caret line="121" column="31" lean-forward="false" selection-start-line="121" selection-start-column="31" selection-end-line="121" selection-end-column="31" />[m
[31m-          <folding />[m
[32m+[m[32m        <state relative-caret-position="1407">[m
[32m+[m[32m          <caret line="73" column="29" lean-forward="false" selection-start-line="73" selection-start-column="29" selection-end-line="73" selection-end-column="29" />[m
[32m+[m[32m          <folding>[m
[32m+[m[32m            <marker date="1488832020602" expanded="true" signature="623:1235" ph="'''...'''" />[m
[32m+[m[32m          </folding>[m
         </state>[m
       </provider>[m
     </entry>[m
[31m-    <entry file="file://$PROJECT_DIR$/faceSpoofValidation.py">[m
[32m+[m[32m    <entry file="file://$PROJECT_DIR$/testingLBP.py">[m
       <provider selected="true" editor-type-id="text-editor">[m
[31m-        <state relative-caret-position="105">[m
[31m-          <caret line="6" column="38" lean-forward="false" selection-start-line="6" selection-start-column="38" selection-end-line="6" selection-end-column="38" />[m
[32m+[m[32m        <state relative-caret-position="-1696">[m
[32m+[m[32m          <caret line="15" column="41" lean-forward="false" selection-start-line="15" selection-start-column="41" selection-end-line="15" selection-end-column="41" />[m
           <folding />[m
         </state>[m
       </provider>[m
     </entry>[m
[31m-    <entry file="file://$PROJECT_DIR$/vlfeatTest.py">[m
[32m+[m[32m    <entry file="file://$PROJECT_DIR$/alignDlibDemo.py">[m
       <provider selected="true" editor-type-id="text-editor">[m
[31m-        <state relative-caret-position="336">[m
[31m-          <caret line="16" column="0" lean-forward="false" selection-start-line="16" selection-start-column="0" selection-end-line="16" selection-end-column="0" />[m
[32m+[m[32m        <state relative-caret-position="71">[m
[32m+[m[32m          <caret line="52" column="8" lean-forward="false" selection-start-line="52" selection-start-column="8" selection-end-line="52" selection-end-column="8" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#0#10#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
     </entry>[m
[31m-    <entry file="file://$PROJECT_DIR$/featureSpeedTesting.py">[m
[32m+[m[32m    <entry file="file://$PROJECT_DIR$/features.py">[m
       <provider selected="true" editor-type-id="text-editor">[m
[31m-        <state relative-caret-position="501">[m
[31m-          <caret line="73" column="29" lean-forward="false" selection-start-line="73" selection-start-column="29" selection-end-line="73" selection-end-column="29" />[m
[32m+[m[32m        <state relative-caret-position="467">[m
[32m+[m[32m          <caret line="76" column="0" lean-forward="false" selection-start-line="76" selection-start-column="0" selection-end-line="76" selection-end-column="0" />[m
           <folding>[m
[31m-            <marker date="1488832020602" expanded="true" signature="623:1235" ph="'''...'''" />[m
[32m+[m[32m            <element signature="e#0#18#0" expanded="true" />[m
           </folding>[m
         </state>[m
       </provider>[m
     </entry>[m
[31m-    <entry file="file://$PROJECT_DIR$/features.py">[m
[32m+[m[32m    <entry file="file://$PROJECT_DIR$/main.py">[m
       <provider selected="true" editor-type-id="text-editor">[m
[31m-        <state relative-caret-position="551">[m
[31m-          <caret line="75" column="22" lean-forward="false" selection-start-line="75" selection-start-column="22" selection-end-line="75" selection-end-column="22" />[m
[32m+[m[32m        <state relative-caret-position="1911">[m
[32m+[m[32m          <caret line="139" column="52" lean-forward="false" selection-start-line="139" selection-start-column="52" selection-end-line="139" selection-end-column="52" />[m
           <folding>[m
[31m-            <element signature="e#0#27#0" expanded="true" />[m
[32m+[m[32m            <element signature="e#427#1455#0" expanded="false" />[m
           </folding>[m
         </state>[m
       </provider>[m
     </entry>[m
[31m-    <entry file="file://$PROJECT_DIR$/alignDlibDemo.py">[m
[32m+[m[32m    <entry file="file://$PROJECT_DIR$/faceSpoofValidation.py">[m
       <provider selected="true" editor-type-id="text-editor">[m
[31m-        <state relative-caret-position="147">[m
[31m-          <caret line="70" column="0" lean-forward="false" selection-start-line="70" selection-start-column="0" selection-end-line="70" selection-end-column="0" />[m
[32m+[m[32m        <state relative-caret-position="441">[m
[32m+[m[32m          <caret line="21" column="31" lean-forward="false" selection-start-line="21" selection-start-column="31" selection-end-line="21" selection-end-column="31" />[m
           <folding>[m
             <element signature="e#0#10#0" expanded="true" />[m
           </folding>[m
[1mdiff --git a/Face spoof detection/Implementation/alignDlibDemo.py b/Face spoof detection/Implementation/alignDlibDemo.py[m
[1mindex 5b910a4..400593e 100644[m
[1m--- a/Face spoof detection/Implementation/alignDlibDemo.py[m	
[1m+++ b/Face spoof detection/Implementation/alignDlibDemo.py[m	
[36m@@ -81,11 +81,9 @@[m [mwhile True:[m
 [m
         cv2kp = [cv2.KeyPoint(x, y, size) for (x,y) in itertools.izip(kp[0], kp[1])][m
 [m
[31m-        print('face dimm', face.shape)[m
 [m
         img = cv2.drawKeypoints(face, cv2kp, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)[m
         cv2.imshow('kp', img)[m
[31m-        print('printed img dim', img.shape)[m
 [m
         startMLBP = time.time()[m
         lbpFeatures.append(mlbp.computeFeaturePatchWise(redFace))[m
[1mdiff --git a/Face spoof detection/Implementation/faceSpoofValidation.py b/Face spoof detection/Implementation/faceSpoofValidation.py[m
[1mindex 8ff5878..5654b04 100644[m
[1m--- a/Face spoof detection/Implementation/faceSpoofValidation.py[m	
[1m+++ b/Face spoof detection/Implementation/faceSpoofValidation.py[m	
[36m@@ -1,5 +1,5 @@[m
 import cv2[m
[31m-import matplotlib.pyplot as plt[m
[32m+[m[32mimport random[m
 [m
 class FaceSpoofValidator:[m
     def __init__(self, lbp):[m
[36m@@ -11,10 +11,15 @@[m [mclass FaceSpoofValidator:[m
 [m
         greyAlignedFace = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)[m
 [m
[31m-        hist, bins, lbpFV = self._lbp.compute(greyAlignedFace)[m
[32m+[m[32m        mlbpFeature = self._lbp.computeFeaturePatchWise(greyAlignedFace)[m
 [m
         #Get the classification for hist[m
 [m
[31m-        cv2.imshow('LBP', lbpFV)[m
[32m+[m[32m        #cv2.imshow('LBP', lbpFV)[m
 [m
         print("Aligned face size {}".format(face.shape))[m
[32m+[m
[32m+[m[32m        if random.random() > 0.2:[m
[32m+[m[32m            return True[m
[32m+[m[32m        else:[m
[32m+[m[32m            return False[m
\ No newline at end of file[m
[1mdiff --git a/Face spoof detection/Implementation/features.py b/Face spoof detection/Implementation/features.py[m
[1mindex 6e3dc49..e8d248e 100644[m
[1m--- a/Face spoof detection/Implementation/features.py[m	
[1m+++ b/Face spoof detection/Implementation/features.py[m	
[36m@@ -1,5 +1,6 @@[m
[31m-from skimage import feature[m
 import numpy as np[m
[32m+[m[32mfrom skimage import feature[m
[32m+[m[32mfrom vlfeat import vl_dsift[m
 import cv2[m
 [m
 [m
[36m@@ -67,11 +68,10 @@[m [mclass MultiScaleLocalBinaryPatterns:[m
 [m
         return lbpFeature[m
 [m
[31m-from vlfeat import vl_dsift[m
[32m+[m
 [m
 class DSIFT:[m
     def compute(self, image, step, size):[m
         kp, desc = vl_dsift(image, step = step, size = size, fast=True)[m
 [m
[31m-[m
         return kp, desc[m
[1mdiff --git a/Face spoof detection/Implementation/main.py b/Face spoof detection/Implementation/main.py[m
[1mindex 94b5722..2117608 100644[m
[1m--- a/Face spoof detection/Implementation/main.py[m	
[1m+++ b/Face spoof detection/Implementation/main.py[m	
[36m@@ -44,7 +44,7 @@[m [mdef initializeParser():[m
                         default=0.5)[m
     return parser[m
 [m
[31m-def processFrame(rgbImage, align, args):[m
[32m+[m[32mdef processFrame(rgbImage, align, faceSpoofValidator, args):[m
     start = time.time()[m
 [m
     if rgbImage is None:[m
[36m@@ -57,7 +57,7 @@[m [mdef processFrame(rgbImage, align, args):[m
         print("Loading the image took {} seconds.".format(time.time() - start))[m
 [m
     originalRGBImage = rgbImage[m
[31m-    rgbImage = cv2.resize(rgbImage, (0,0), args.scaleX, args.scaleY)[m
[32m+[m[32m    rgbImage = cv2.resize(rgbImage, (0,0), fx=args.scaleX, fy=args.scaleY)[m
 [m
     start = time.time()[m
 [m
[36m@@ -93,10 +93,10 @@[m [mdef processFrame(rgbImage, align, args):[m
     facesWithValidation= [][m
 [m
     for i, alignedFace in enumerate(alignedFaces):[m
[31m-        if faceSpoofValidation.validateFace(alignedFace, lbp):[m
[31m-            facesWithValidation.append((alignedFace, 1))[m
[32m+[m[32m        if faceSpoofValidator.validateFace(alignedFace):[m
[32m+[m[32m            facesWithValidation.append((alignedFace, bb[i], 1))[m
         else:[m
[31m-            facesWithValidation.append((alignedFace, 0))[m
[32m+[m[32m            facesWithValidation.append((alignedFace, bb[i], 0))[m
 [m
     return facesWithValidation[m
 [m
[36m@@ -112,6 +112,7 @@[m [mdef main():[m
     frameNr = 0[m
 [m
     align = openface.AlignDlib(args.dlibFacePredictor)[m
[32m+[m[32m    faceSpoofValidator = faceSpoofValidation.FaceSpoofValidator(features.MultiScaleLocalBinaryPatterns())[m
     while True:[m
         ret, frame = video_capture.read()[m
 [m
[36m@@ -125,10 +126,24 @@[m [mdef main():[m
         start = time.time()[m
 [m
         #Get the faces in the frame that are not spoof[m
[31m-        facesWithValidation = processFrame(frame, align, args)[m
[32m+[m[32m        facesWithValidation = processFrame(frame, align, faceSpoofValidator, args)[m
 [m
         #Process here faces having their validation[m
 [m
[32m+[m[32m        for faceWithValidation in facesWithValidation:[m
[32m+[m[32m            bb = faceWithValidation[1][m
[32m+[m
[32m+[m[32m            ll = (int(round(bb.left()/args.scaleX)),int(round(bb.bottom()/args.scaleY)))[m
[32m+[m[32m            ur = (int(round(bb.right()/args.scaleX)), int(round(bb.top()/args.scaleY)))[m
[32m+[m
[32m+[m[32m            if faceWithValidation[2] == 1:[m
[32m+[m[32m                cv2.rectangle(frame, ll, ur, color=(0, 255, 0),thickness=3)[m
[32m+[m[32m            else:[m
[32m+[m[32m                cv2.rectangle(frame, ll, ur, color=(0, 0, 255), thickness=3)[m
[32m+[m
[32m+[m[32m        cv2.imshow('face', frame)[m
[32m+[m[32m        if cv2.waitKey(1) & 0xFF == ord('q'):[m
[32m+[m[32m            break[m
         print("Entire processing of a frame took {}".format(time.time() - start))[m
 [m
     video_capture.release()[m
