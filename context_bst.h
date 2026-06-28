#ifndef CONTEXT_BST_H
#define CONTEXT_BST_H

typedef struct NodeBST NodeBST;
NodeBST* insert_context_node(NodeBST* root, int score, const char* txt);
void gather_high_intent_context(NodeBST* root, int min_score, char* output_buffer);
void clear_context_tree(NodeBST* root);

#endif
