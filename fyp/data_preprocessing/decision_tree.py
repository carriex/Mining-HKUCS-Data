import sklearn

def convert_feature(features):
	feature_names = {'toefl':'TOEFL','gpa_ug_scale':'Unergraduate_GPA','papers':'Papers','major_ug':'Undergrad_Major_','qs_ug':'Undergraduate_QS'}
	for f in features:
		if f in feature_names:
			features[features.index(f)] = feature_names[f]
	return features  


def treeToJson(decision_tree, feature_names=None, class_names=None):
	from warnings import warn
 
	js = ""
 
	def node_to_str(tree, node_id, criterion):
		if not isinstance(criterion, sklearn.tree.tree.six.string_types):
			criterion = "impurity"
 
		value = tree.value[node_id]
		if tree.n_outputs == 1:
			value = value[0, :]
		jsonValue = ', '.join([str(x) for x in value])


		#jsonValue = str(list(zip(class_names, jsonValue.split(','))))
		newJson = []
		max_class = ''
		max_value = 0
		for (c,v) in zip(class_names, jsonValue.split(',')):
			newJson.append({c:int(float(v))})
			if class_names.index(c) > 0 and int(float(v)) > max_value:
				max_value = int(float(v))
				max_class = c

		jsonValue = str(newJson)
		max_value = str(max_value)

		if tree.children_left[node_id] == sklearn.tree._tree.TREE_LEAF:
			return '"id": "%s", "criterion": "%s", "impurity": "%s", "samples": "%s", "value": "%s", "max_class": "%s", "max_value":"%s"' \
						 % (node_id, 
								criterion,
								tree.impurity[node_id],
								tree.n_node_samples[node_id],
								jsonValue,
								max_class,
								max_value)
		else:
			if feature_names is not None:
				feature = feature_names[tree.feature[node_id]]
			else:
				feature = tree.feature[node_id]
 
			if "=" == feature:
				ruleType = "="
				ruleValue = "false"
			elif "Major" in feature:
				ruleType = "not_"
				ruleValue = "CS"
			else:
				ruleType = "<="
				ruleValue = "%.4f" % tree.threshold[node_id]
 
			return '"id": "%s", "name": "%s %s %s", "%s": "%s", "samples": "%s"' \
						 % (node_id, 
								feature,
								ruleType,
								ruleValue,
								criterion,
								tree.impurity[node_id],
								tree.n_node_samples[node_id])
 
	def recurse(tree, node_id, criterion, parent=None, depth=0):
		tabs = "  " * depth
		js = ""
 
		left_child = tree.children_left[node_id]
		right_child = tree.children_right[node_id]
 
		js = js + "\n" + \
				 tabs + "{\n" + \
				 tabs + "  " + node_to_str(tree, node_id, criterion)
 
		if left_child != sklearn.tree._tree.TREE_LEAF:
			js = js + ",\n" + \
					 tabs + '  "children":[ ' + \
					 recurse(tree, \
									 left_child, \
									 criterion=criterion, \
									 parent=node_id, \
									 depth=depth + 1) + "\n" + \
					 tabs + ',' + \
					 recurse(tree, \
									 right_child, \
									 criterion=criterion, \
									 parent=node_id,
									 depth=depth + 1) + \
					 tabs + ']'
		js = js + tabs + "\n" + \
				 tabs + "}"
 
		return js
 
	if isinstance(decision_tree, sklearn.tree.tree.Tree):
		js = js + recurse(decision_tree, 0, criterion="impurity")
	else:
		js = js + recurse(decision_tree.tree_, 0, criterion=decision_tree.criterion)
 
	return js