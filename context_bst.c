#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct NodeBST {
    int key_score; // Sorted index ranking representation based on anomaly scores
    char summary_text[128];
    struct NodeBST* left;
    struct NodeBST* right;
} NodeBST;

NodeBST* create_bst_node(int score, const char* txt) {
    NodeBST* node = (NodeBST*)malloc(sizeof(NodeBST));
    if (node) {
        node->key_score = score;
        strncpy(node->summary_text, txt, sizeof(node->summary_text) - 1);
        node->left = NULL;
        node->right = NULL;
    }
    return node;
}

#ifdef _WIN32
    __declspec(dllexport) NodeBST* insert_context_node(NodeBST* root, int score, const char* txt);
    __declspec(dllexport) void gather_high_intent_context(NodeBST* root, int min_score, char* output_buffer);
    __declspec(dllexport) void clear_context_tree(NodeBST* root);
#endif

NodeBST* insert_context_node(NodeBST* root, int score, const char* txt) {
    if (!root) return create_bst_node(score, txt);
    if (score < root->key_score) root->left = insert_context_node(root->left, score, txt);
    else root->right = insert_context_node(root->right, score, txt);
    return root;
}

// In-order traversal across structural branches to extract context details above specific alert levels
void gather_high_intent_context(NodeBST* root, int min_score, char* output_buffer) {
    if (!root) return;
    gather_high_intent_context(root->left, min_score, output_buffer);
    if (root->key_score >= min_score) {
        strcat(output_buffer, root->summary_text);
        strcat(output_buffer, " | ");
    }
    gather_high_intent_context(root->right, min_score, output_buffer);
}

void clear_context_tree(NodeBST* root) {
    if (!root) return;
    clear_context_tree(root->left);
    clear_context_tree(root->right);
    free(root);
}
