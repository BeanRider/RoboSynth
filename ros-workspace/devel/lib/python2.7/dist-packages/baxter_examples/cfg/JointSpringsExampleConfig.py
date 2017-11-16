## *********************************************************
##
## File autogenerated for the joint_torque package
## by the dynamic_reconfigure package.
## Please do not edit.
##
## ********************************************************/

from dynamic_reconfigure.encoding import extract_params

inf = float('inf')

config_description = {'upper': 'DEFAULT', 'lower': 'groups', 'srcline': 245, 'name': 'Default', 'parent': 0, 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'cstate': 'true', 'parentname': 'Default', 'class': 'DEFAULT', 'field': 'default', 'state': True, 'parentclass': '', 'groups': [], 'parameters': [{'srcline': 292, 'description': "s0 - Joint spring stiffness (k). Hooke's Law.", 'max': 30.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 's0_spring_stiffness', 'edit_method': '', 'default': 10.0, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': 's0 - Joint damping coefficient (c).', 'max': 10.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 's0_damping_coefficient', 'edit_method': '', 'default': 0.1, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': "s1 - Joint spring stiffness (k). Hooke's Law.", 'max': 30.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 's1_spring_stiffness', 'edit_method': '', 'default': 15.0, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': 's1 - Joint damping coefficient (c).', 'max': 7.5, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 's1_damping_coefficient', 'edit_method': '', 'default': 0.1, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': "e0 - Joint spring stiffness (k). Hooke's Law.", 'max': 15.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 'e0_spring_stiffness', 'edit_method': '', 'default': 5.0, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': 'e0 - Joint damping coefficient (c).', 'max': 7.5, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 'e0_damping_coefficient', 'edit_method': '', 'default': 0.1, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': "e1 - Joint spring stiffness (k). Hooke's Law.", 'max': 15.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 'e1_spring_stiffness', 'edit_method': '', 'default': 5.0, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': 'e1 - Joint damping coefficient (c).', 'max': 5.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 'e1_damping_coefficient', 'edit_method': '', 'default': 0.1, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': "w0 - Joint spring stiffness (k). Hooke's Law.", 'max': 9.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 'w0_spring_stiffness', 'edit_method': '', 'default': 3.0, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': 'w0 - Joint damping coefficient (c).', 'max': 1.5, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 'w0_damping_coefficient', 'edit_method': '', 'default': 0.1, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': "w1 - Joint spring stiffness (k). Hooke's Law.", 'max': 4.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 'w1_spring_stiffness', 'edit_method': '', 'default': 2.0, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': 'w1 - Joint damping coefficient (c).', 'max': 1.5, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 'w1_damping_coefficient', 'edit_method': '', 'default': 0.1, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': "w2 - Joint spring stiffness (k). Hooke's Law.", 'max': 4.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 'w2_spring_stiffness', 'edit_method': '', 'default': 1.5, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 292, 'description': 'w2 - Joint damping coefficient (c).', 'max': 1.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/opt/ros/lunar/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'name': 'w2_damping_coefficient', 'edit_method': '', 'default': 0.1, 'level': 0, 'min': 0.0, 'type': 'double'}], 'type': '', 'id': 0}

min = {}
max = {}
defaults = {}
level = {}
type = {}
all_level = 0

#def extract_params(config):
#    params = []
#    params.extend(config['parameters'])
#    for group in config['groups']:
#        params.extend(extract_params(group))
#    return params

for param in extract_params(config_description):
    min[param['name']] = param['min']
    max[param['name']] = param['max']
    defaults[param['name']] = param['default']
    level[param['name']] = param['level']
    type[param['name']] = param['type']
    all_level = all_level | param['level']

