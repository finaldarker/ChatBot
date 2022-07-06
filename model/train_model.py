from model.encoder_decoder import encoder, decoder, trainIters, model_name, voc, pairs, embedding, \
    encoder_n_layers, \
    decoder_n_layers, save_dir, n_iteration, batch_size, print_every, save_every, clip, corpus_name, \
    GreedySearchDecoder, evaluateInput, encoder_optimizer, decoder_optimizer, loadFilename

# 设置进入训练模式，从而开启dropout
encoder.train()
decoder.train()
# 开始训练
print("Starting Training!")
trainIters(model_name
           , voc, pairs, encoder, decoder, encoder_optimizer, decoder_optimizer,
           embedding, encoder_n_layers, decoder_n_layers, save_dir, n_iteration, batch_size,
           print_every, save_every, clip, corpus_name, loadFilename)
# 进入eval模式，从而去掉dropout。
encoder.eval()
decoder.eval()
# 构造searcher对象
searcher = GreedySearchDecoder(encoder, decoder)
# 测试
evaluateInput(encoder, decoder, searcher, voc)
