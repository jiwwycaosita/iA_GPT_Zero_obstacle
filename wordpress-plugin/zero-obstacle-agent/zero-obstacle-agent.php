<?php
/**
 * Plugin Name: Zero Obstacle Agent
 * Description: Connecte WordPress à ton orchestrateur d'agents Zero Obstacle (FastAPI sur ton PC).
 * Version: 0.1.0
 * Author: Zero Obstacle IA
 */

if (!defined('ABSPATH')) {
    exit;
}

// Option pour stocker l'URL de l'API (ex: http://192.168.0.10:8080)
function zoa_register_settings() {
    add_option('zoa_api_url', 'http://localhost:8080');
    register_setting('zoa_options_group', 'zoa_api_url', 'esc_url_raw');
}
add_action('admin_init', 'zoa_register_settings');

function zoa_register_options_page() {
    add_options_page('Zero Obstacle Agent', 'Zero Obstacle Agent', 'manage_options', 'zoa', 'zoa_options_page');
}
add_action('admin_menu', 'zoa_register_options_page');

function zoa_options_page() {
    ?>
    <div class="wrap">
        <h1>Zero Obstacle Agent</h1>
        <form method="post" action="options.php">
            <?php settings_fields('zoa_options_group'); ?>
            <table class="form-table">
                <tr valign="top">
                    <th scope="row">URL de l'API FastAPI</th>
                    <td>
                        <input type="text" name="zoa_api_url" style="width: 400px;"
                               value="<?php echo esc_attr(get_option('zoa_api_url')); ?>" />
                        <p class="description">Ex: http://TON_PC:8080</p>
                    </td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

// Shortcode [zero_obstacle_form]
function zoa_form_shortcode() {
    $api_url = esc_url(get_option('zoa_api_url'));

    $form_output = '';

    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['zoa_question']) && check_admin_referer('zoa_form_action', 'zoa_form_nonce')) {
        $user_question = sanitize_textarea_field($_POST['zoa_question']);

        $api_request_body = wp_json_encode(array(
            'task' => 'general',
            'text' => $user_question,
        ));

        $api_response = wp_remote_post(rtrim($api_url, '/') . '/agent/orchestrate', array(
            'headers' => array('Content-Type' => 'application/json'),
            'body'    => $api_request_body,
            'timeout' => 60,
        ));

        if (is_wp_error($api_response)) {
            $form_output .= '<div style="color:red;">Erreur de connexion à l’agent : ' . esc_html($api_response->get_error_message()) . '</div>';
        } else {
            $http_status_code = wp_remote_retrieve_response_code($api_response);
            $api_response_body = wp_remote_retrieve_body($api_response);
            if ($http_status_code === 200) {
                $response_data = json_decode($api_response_body, true);
                $agent_answer = isset($response_data['result']['answer']) ? esc_html($response_data['result']['answer']) : 'Aucune réponse.';
                $form_output .= '<h3>Réponse de l’agent :</h3><pre style="white-space:pre-wrap;">' . $agent_answer . '</pre>';
            } else {
                $form_output .= '<div style="color:red;">Erreur API (' . intval($http_status_code) . ') : ' . esc_html($api_response_body) . '</div>';
            }
        }
    }

    ob_start();
    ?>
    <form method="post">
        <?php wp_nonce_field('zoa_form_action', 'zoa_form_nonce'); ?>
        <p>
            <label for="zoa_question">Votre question pour Zéro Obstacle :</label><br>
            <textarea id="zoa_question" name="zoa_question" rows="5" cols="60" required></textarea>
        </p>
        <p>
            <button type="submit">Envoyer à l’agent</button>
        </p>
    </form>
    <?php
    $form_html = ob_get_clean();

    return $form_output . $form_html;
}
add_shortcode('zero_obstacle_form', 'zoa_form_shortcode');
